import random
import logging

logger = logging.getLogger(__name__)

# Try to load spaCy, but fallback gracefully if it fails (e.g. Python 3.14 compatibility)
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Model not found, try to download or just warn
        logger.warning("spaCy model 'en_core_web_sm' not found. Grammar transformation will be disabled.")
        nlp = None
    except Exception as e:
         logger.warning(f"spaCy model failed to load due to error: {e}. Grammar transformation will be disabled.")
         nlp = None
except ImportError:
    logger.warning("spaCy library not found. Grammar transformation will be disabled.")
    nlp = None
except Exception as e:
    # Catching Pydantic/ConfigError on Python 3.14
    logger.warning(f"spaCy failed to import (likely Python 3.14 compatibility): {e}. Grammar transformation will be disabled.")
    nlp = None

def transform_to_osv(text: str) -> str:
    """
    Attempt to transform an English sentence into Object-Subject-Verb (OSV) order.
    Refines the output from the LLM to strictly enforce the Jedi grammar where possible.
    Includes safety checks to only transform when a clear S-V-O structure is identified.
    """
    if nlp is None:
        return text

    try:
        doc = nlp(text)
        sentences = list(doc.sents)
        transformed_sentences = []

        for sent in sentences:
            # Simple heuristic for safety: don't transform questions or very short sentences
            if sent.text.strip().endswith("?") or len(sent) < 4:
                transformed_sentences.append(sent.text)
                continue
                
            root = sent.root
            subj = None
            dobj = None
            
            # Find subject and direct object
            for child in root.children:
                if child.dep_ == "nsubj":
                    subj = child
                elif child.dep_ == "dobj":
                    dobj = child
            
            # Check if we have a standard SVO pattern
            if subj and dobj and root.pos_ == "VERB":
                # Construct OSV: Object -> Subject -> Verb
                
                # Get subtree text for each component to keep adjectives/modifiers attached
                subj_text = "".join([t.text_with_ws for t in subj.subtree]).strip()
                dobj_text = "".join([t.text_with_ws for t in dobj.subtree]).strip()
                
                # Get the verb and any auxiliaries (like "will", "can")
                aux = [child for child in root.children if child.dep_ == "aux"]
                aux_text = " ".join([a.text for a in aux])
                
                # Basic verb phrase construction
                verb_text = root.text
                if aux_text:
                    # Simpler: "You must learn patience" -> "Patience, you must learn."
                    # We reconstructed logic slightly for better flow
                    verb_part = f"{aux_text} {verb_text}".strip()
                else:
                    verb_part = verb_text
                
                # Capitalize object if it starts the sentence
                dobj_text = dobj_text[0].upper() + dobj_text[1:] if dobj_text else dobj_text
                # Lowercase subject if it follows
                subj_text = subj_text[0].lower() + subj_text[1:] if subj_text and not subj.ent_type_ else subj_text

                # Construct the sentence
                transformed_sent = f"{dobj_text}, {subj_text} {verb_part}."
                transformed_sentences.append(transformed_sent)
            else:
                # Fallback: keep original if structure isn't clear
                transformed_sentences.append(sent.text)

        return " ".join(transformed_sentences)
    except Exception as e:
        logger.error(f"Error during grammar transformation: {e}")
        return text
