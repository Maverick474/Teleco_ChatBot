<<<<<<< HEAD
from typing import TypedDict, List, Optional, Dict, Annotated, Sequence
=======
from typing import TypedDict, List, Optional, Dict
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
from langchain_openai import ChatOpenAI
import os
from vectordb import VectorDBManager
from datetime import datetime
<<<<<<< HEAD
import random
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
=======
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20

# Initialize LLM
llm = ChatOpenAI(
    model='gpt-4o-mini',
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

# Initialize vector database manager
vector_manager = VectorDBManager()

# Conversation memory
conversation_memory: Dict[str, Dict] = {}

# TIGHTENED: Only these three languages are supported
SUPPORTED_LANGUAGES = {
    'en': ['bill', 'plan', 'internet', 'router', 'outage', 'package', 'data', 'payment', 'policy', 'teleco', 'sim', 'network', 'phone', 'mobile', 'call', 'signal'],
    'ur': ['بل', 'پلان', 'انٹرنیٹ', 'راوٹر', 'ان آؤٹیج', 'پیکیج', 'ڈیٹا', 'ادائیگی', 'پالیسی', 'ٹیلیکو', 'سم', 'نیٹورک', 'فون', 'موبائل', 'کال', 'سگنل'],
    'ar': ['فاتورة', 'خطة', 'الانترنت', 'الراوٹر', 'انقطاع', 'حزمة', 'بيانات', 'دفع', 'سياسة', 'تيليكوم', 'شريحة', 'شبكة', 'هاتف', 'موبايل', 'مكالمة', 'إشارة']
}

# STRICT: Category keywords for validation
CATEGORY_KEYWORDS = {
    'billing': ['bill', 'payment', 'invoice', 'charge', 'fee', 'overage', 'balance', 'due', 'statement'],
    'packages': ['plan', 'package', 'data', 'upgrade', 'downgrade', 'roaming', 'premium', 'basic', 'plan'],
    'troubleshooting': ['router', 'internet', 'connection', 'outage', 'speed', 'reboot', 'reset', 'signal', 'wifi', 'sim', 'network', 'phone', 'mobile', 'call', 'not working', 'problem', 'issue', 'error', 'slow', 'disconnected'],
    'policies': ['policy', 'terms', 'conditions', 'sla', 'guarantee', 'credit', 'refund', 'compensation'],
    'general': ['teleco', 'service', 'services', 'about', 'company', 'what is', 'tell me', 'information', 'offer', 'provide']
}

<<<<<<< HEAD
class State(TypedDict):
    # Input
    text: str
    conversation_id: Optional[str]
    is_new_conversation: bool
    
    # Processing
    language: str
    original_language: str
    english_query: Optional[str]
    previous_intent: Optional[str]
    
    # Routing
    current_route: str
    agent_path: List[str]
    
    # Context & Memory
    context: Optional[str]
    user_name: Optional[str]
    
    # Output
    response: Optional[str]
    should_end: bool
    is_greeting: bool
    is_farewell: bool
=======
class TelecoState(TypedDict):
    text: str
    language: str 
    original_language: str 
    route: Optional[str]
    agent_path: List[str]
    response: Optional[str]
    context: Optional[str]
    conversation_id: Optional[str]
    user_name: Optional[str]
    is_new_conversation: bool
    previous_intent: Optional[str]
    # NEW: Store English version of the query for processing
    english_query: Optional[str]
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20

class HumanoidResponse(TypedDict):
    response: str
    agent_path: List[str]
    language: str
    conversation_id: str
    is_greeting: bool
    is_farewell: bool

def rag_retrieve(query_en: str, category: str) -> str:
    """ChromaDB-powered retrieval with category filtering"""
<<<<<<< HEAD
    if category == "general":
        results = vector_manager.similarity_search(
            query_en,
            k=5,
            filter=None
        )
    else:
=======
    # For "general" queries, search ALL documents without category filter
    # because general info about Teleco could be in any document
    if category == "general":
        results = vector_manager.similarity_search(
            query_en,
            k=5,  # Get more results for general queries
            filter=None  # No category filter
        )
    else:
        # First try with category filter
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        results = vector_manager.similarity_search(
            query_en,
            k=3,
            filter={"category": category}
        )
        
<<<<<<< HEAD
=======
        # If no results found with category filter, try without filter
        # This handles cases where documents might not be categorized correctly
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        if not results:
            print(f"No results with category '{category}', searching all documents...")
            results = vector_manager.similarity_search(
                query_en,
                k=3,
                filter=None
            )
    
    formatted_results = []
    for i, doc in enumerate(results, 1):
        title = doc.metadata.get("title", "Unknown")
        doc_category = doc.metadata.get("category", "Unknown")
        formatted_results.append(
            f"Reference #{i} ({title} - {doc_category}):\n{doc.page_content}"
        )
    
    return "\n\n".join(formatted_results) if formatted_results else ""

<<<<<<< HEAD
=======
# ===== ENHANCED TRANSLATION UTILITIES =====
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
def translate_text(text: str, src_lang: str, target_lang: str) -> str:
    """Translate text between languages"""
    if src_lang == target_lang:
        return text
    
<<<<<<< HEAD
=======
    # Map Teleco brand name to target language script
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    teleco_in_target = {
        'en': 'Teleco',
        'ur': 'ٹیلیکو',
        'ar': 'تيليكو'
    }
    
    prompt = f"""
    Translate the following text from {src_lang} to {target_lang}.
    Write the brand name "Teleco" as "{teleco_in_target.get(target_lang, 'Teleco')}" in your translation.
    Translate EVERYTHING to {target_lang} script - no English words should remain.
    Maintain professional tone and preserve all numbers.
    
    Text: {text}
    
    Translation (pure {target_lang} only, no English):
    """
    return llm.invoke(prompt).content.strip()

def translate_to_english(text: str, src_lang: str) -> str:
    """Translate non-English text to English"""
    if src_lang == 'en':
        return text
    return translate_text(text, src_lang, 'en')

def translate_response(text: str, target_lang: str) -> str:
    """Translate English response to target language"""
    if target_lang == 'en':
        return text
    return translate_text(text, 'en', target_lang)

<<<<<<< HEAD
=======
# ===== NEW TRANSLATION NODE =====
def translation_node(state: TelecoState):
    """Translate query to English for processing and store English query in state"""
    if state["language"] == 'en':
        # If already English, just copy text to english_query
        state["english_query"] = state["text"]
    else:
        # Translate non-English query to English
        state["english_query"] = translate_to_english(state["text"], state["language"])
    
    state["agent_path"].append("TranslationNode")
    return state

# ===== LLM-GENERATED GREETING/FAREWELL FUNCTIONS =====
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
def get_random_greeting(language: str, user_name: Optional[str] = None) -> str:
    """Generate a humanoid greeting using LLM"""
    time_of_day = get_time_based_greeting()
    
<<<<<<< HEAD
=======
    # Add some variation hints
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    style_hints = [
        "Be enthusiastic and warm",
        "Be calm and professional", 
        "Be casual and friendly",
        "Be cheerful and welcoming"
    ]
<<<<<<< HEAD
=======
    import random
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    style = random.choice(style_hints)
    
    prompt = f"""
    Generate a unique, warm greeting for a Teleco customer service chatbot.
    
    Requirements:
    - Language: {language} ({'English' if language == 'en' else 'Urdu' if language == 'ur' else 'Arabic'})
    - Time of day: {time_of_day}
    - Customer name: {user_name if user_name else 'Not provided - do not use a name'}
    - Company: Teleco (telecommunications company)
    - Style: {style}
    
    IMPORTANT:
    - Generate a UNIQUE greeting - be creative!
    - Sound like a friendly, helpful human - not robotic
    - Mention you can help with Teleco services
    - Keep it brief (1-2 sentences)
    - {'Address the customer by name naturally' if user_name else 'Do not use any name placeholder'}
    
    Generate ONLY the greeting message in {language}, nothing else:
    """
    
    try:
        return llm.invoke(prompt).content.strip()
    except:
<<<<<<< HEAD
=======
        # Fallback if LLM fails
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        if language == 'en':
            return f"Hello{f' {user_name}' if user_name else ''}! How can I help you with Teleco services today?"
        elif language == 'ur':
            return f"السلام علیکم{f' {user_name}' if user_name else ''}! میں آج آپ کی کس طرح مدد کر سکتا ہوں؟"
        else:
            return f"مرحباً{f' {user_name}' if user_name else ''}! كيف يمكنني مساعدتك اليوم؟"

def get_random_farewell(language: str, user_name: Optional[str] = None, issue_resolved: bool = False) -> str:
    """Generate a humanoid farewell using LLM"""
<<<<<<< HEAD
=======
    
    # Add some variation hints
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    style_hints = [
        "Be warm and appreciative",
        "Be cheerful and positive",
        "Be friendly and inviting",
        "Be casual and kind"
    ]
<<<<<<< HEAD
=======
    import random
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    style = random.choice(style_hints)
    
    prompt = f"""
    Generate a unique, warm farewell for a Teleco customer service chatbot.
    
    Requirements:
    - Language: {language} ({'English' if language == 'en' else 'Urdu' if language == 'ur' else 'Arabic'})
    - Customer name: {user_name if user_name else 'Not provided - do not use a name'}
    - Company: Teleco (telecommunications company)
    - Style: {style}
    
    Context:
    {"The customer had an issue that was resolved - express happiness that you could help!" if issue_resolved else "This is a simple goodbye - just wish them well and invite them to return anytime they need help. Do NOT apologize or imply there was an unresolved issue."}
    
    IMPORTANT:
    - Generate a UNIQUE farewell - be creative!
    - Sound like a friendly human, not robotic
    - Keep it brief (1-2 sentences)
    - {'Address the customer by name naturally' if user_name else 'Do not use any name placeholder'}
    - Do NOT apologize unless an issue was actually unresolved
    
    Generate ONLY the farewell message in {language}, nothing else:
    """
    
    try:
        return llm.invoke(prompt).content.strip()
    except:
<<<<<<< HEAD
=======
        # Fallback if LLM fails
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        if language == 'en':
            base = "Glad I could help!" if issue_resolved else "Goodbye!"
            return f"{base}{f' {user_name},' if user_name else ''} Have a great day!"
        elif language == 'ur':
            base = "خوشی ہوئی کہ میں مدد کر سکا!" if issue_resolved else "الوداع!"
            return f"{base}{f' {user_name},' if user_name else ''} آپ کا دن اچھا گزرے!"
        else:
            base = "سعيد لأنني استطعت المساعدة!" if issue_resolved else "وداعاً!"
            return f"{base}{f' {user_name},' if user_name else ''} أتمنى لك نهاراً سعيداً!"

<<<<<<< HEAD
def detect_intent_and_teleco_relevance(text: str, language: str) -> tuple[str, bool]:
    """Detect user intent AND check if it's Teleco-related"""
    text_lower = text.lower()
    
    # Check if "teleco" is mentioned in ANY supported language
=======
# ===== HUMANOID ENHANCEMENTS =====
def detect_intent_and_teleco_relevance(state: TelecoState) -> tuple[str, bool]:
    """Detect user intent AND check if it's Teleco-related"""
    text = state["text"]
    language = state["language"]
    
    # First, check for Teleco keywords in the original language
    keywords = SUPPORTED_LANGUAGES[language]
    text_lower = text.lower()
    
    # Check if "teleco" is mentioned in ANY supported language - if so, it's definitely Teleco-related
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    teleco_brand_names = [
        'teleco', 'telco', 'telecom', 
        'ٹیلیکو', 'ٹیلی کو', 'ٹیلکو', 'ٹیلیکوم',  
        'تيليكو', 'تيليكوم', 'تلكو', 'تليكو'  
    ]
<<<<<<< HEAD
    teleco_mentioned = any(brand in text_lower or brand in text for brand in teleco_brand_names)
    has_teleco_keywords = any(kw in text_lower for kw in SUPPORTED_LANGUAGES[language])
    
    if teleco_mentioned:
        return "TELECO_QUERY", True
    
    # Use LLM to detect intent and Teleco relevance
=======
    # Check both lowercase and original text (for non-ASCII characters)
    teleco_mentioned = any(brand in text_lower or brand in text for brand in teleco_brand_names)
    has_teleco_keywords = any(kw in text_lower for kw in keywords)
    
    # If Teleco is mentioned in the query (in ANY language), it's always Teleco-related
    if teleco_mentioned:
        return "TELECO_QUERY", True
    
    # Then use LLM to detect intent and Teleco relevance
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    Analyze the user's message and provide TWO things:
    
    1. INTENT: Classify into ONE category:
       - GREETING: Hello, hi, good morning/evening, etc.
       - FAREWELL: Bye, goodbye, see you, etc.
       - THANKS: Thank you, thanks, gratitude
       - INTRODUCTION: User sharing their name/identity
       - TELECO_QUERY: Query about Teleco services, company, or any telecommunications-related question
       - NON_TELECO_QUERY: Any query NOT related to Teleco or telecommunications
    
    2. TELECO_RELEVANCE: Is this query related to Teleco company, its services, or telecommunications?
       - Answer YES if the query mentions Teleco, asks about telecom services, internet, billing, plans, etc.
       - Answer YES if asking general questions about Teleco company (location, aim, history, services offered)
       - Answer NO only if it's completely unrelated (like asking about weather, geography, general knowledge)
    
    Language: {language}
    Message: {text}
    
    Output format:
    INTENT: [category]
    TELECO_RELEVANCE: [YES/NO]
    """
    
    response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Parse response
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    lines = response.split('\n')
    intent = None
    teleco_relevant = False
    
    for line in lines:
        if line.startswith('INTENT:'):
            intent = line.replace('INTENT:', '').strip()
        elif line.startswith('TELECO_RELEVANCE:'):
            relevance = line.replace('TELECO_RELEVANCE:', '').strip()
            teleco_relevant = (relevance == 'YES')
    
<<<<<<< HEAD
=======
    # If we couldn't parse, fallback to keyword check
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if intent is None:
        intent = "TELECO_QUERY" if has_teleco_keywords else "NON_TELECO_QUERY"
    
    return intent, teleco_relevant or has_teleco_keywords

<<<<<<< HEAD
=======
def generate_humanoid_greeting(language: str, user_name: Optional[str] = None) -> str:
    """Generate personalized greeting using LLM"""
    time_of_day = get_time_based_greeting()
    
    prompt = f"""
    Generate a warm, professional greeting for a telecom customer service chatbot.
    
    Requirements:
    - Language: {language}
    - Time of day: {time_of_day}
    - User name: {user_name if user_name else 'Not provided'}
    - Company: Teleco
    - Tone: Friendly, helpful, professional
    
    {"Include the user's name naturally in the greeting" if user_name else "Don't use name since not provided"}
    Mention that you can help with Teleco services.
    
    Make it sound natural and human-like (1-2 sentences).
    
    Generate ONLY the greeting message in {language}:
    """
    return llm.invoke(prompt).content.strip()

def generate_humanoid_farewell(language: str, user_name: Optional[str] = None, 
                              issue_resolved: bool = False) -> str:
    """Generate personalized farewell using LLM"""
    prompt = f"""
    Generate a warm, professional farewell for a telecom customer service chatbot.
    
    Requirements:
    - Language: {language}
    - User name: {user_name if user_name else 'Not provided'}
    - Issue resolved: {issue_resolved}
    - Company: Teleco
    - Tone: Friendly, appreciative, professional
    
    {"Thank the user by name" if user_name else "Thank generically"}
    {"Add a positive note about resolution" if issue_resolved else "Offer further assistance"}
    
    Make it sound natural and human-like.
    Keep it concise (1-2 sentences).
    
    Generate ONLY the farewell message in {language}:
    """
    return llm.invoke(prompt).content.strip()

>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
def generate_non_teleco_response(language: str, user_query: str) -> str:
    """Generate humanoid, conversational response for non-Teleco queries"""
    prompt = f"""
    You are a friendly, warm Teleco customer service assistant with a conversational personality. 
    A user has asked something that's not about Teleco services.
    
    User's query: {user_query}
    Language: {language}
    
    Generate a NATURAL, HUMANOID response that:
    1. Sounds like a real person chatting, not a robot
    2. Shows warmth and understanding - maybe use a friendly emoji or two
    3. Gently redirects them to Teleco-related topics you can help with
    4. Mentions a couple of things you CAN help with (billing questions, internet issues, plan upgrades, etc.) but don't just list them robotically
    5. Keeps it conversational and brief (2-3 sentences)
    
    STYLE GUIDELINES:
    - Use contractions (I'm, I'd, you're, etc.)
    - Be casual but professional
    - Don't say "I cannot" or "I am unable" - instead focus on what you CAN do
    - Don't list all services in a formal way - mention 1-2 naturally
    - Sound like a helpful friend, not a corporate script
    
    Example good responses:
    - "Haha, I wish I knew! 😄 I'm actually a Teleco helper though - so if you ever need help with your internet, bills, or service plans, that's my jam!"
    - "That's a fun question! I'm more of a telecom whiz though 📱 Got any questions about your Teleco services I could help with?"
    
    Generate ONLY the response in {language}:
    """
    return llm.invoke(prompt).content.strip()

def get_time_based_greeting() -> str:
    """Get appropriate time-based greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def extract_user_name(text: str, language: str) -> Optional[str]:
    """Extract user name from conversation using LLM"""
    prompt = f"""
    Extract the user's name from the following message. If no name is provided, respond with "NOT_PROVIDED".
    
    Language: {language}
    Message: {text}
    
    Respond with ONLY the name or "NOT_PROVIDED":
    """
    response = llm.invoke(prompt).content.strip()
    return response if response != "NOT_PROVIDED" else None

<<<<<<< HEAD
=======
# ===== SPELLING CORRECTION UTILITY =====
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
def correct_spelling_and_normalize(text: str) -> str:
    """Use LLM to correct spelling errors and normalize text while preserving meaning"""
    prompt = f"""
    Analyze the following text and:
    1. Correct any spelling errors
    2. Normalize common variations (e.g., "fare well" -> "farewell", "good bye" -> "goodbye")
    3. IMPORTANT: Correct any misspellings of "Teleco" brand name (e.g., "teleci", "telco", "telecoo", "telico", "telleco", "teelco" should all become "Teleco")
    4. Preserve the original meaning and intent
    5. Keep the same language as input
    
    Input text: {text}
    
    Return ONLY the corrected/normalized text, nothing else:
    """
    try:
        corrected = llm.invoke(prompt).content.strip()
<<<<<<< HEAD
=======
        # Remove quotes if the LLM wrapped the response
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        corrected = corrected.strip('"').strip("'")
        return corrected if corrected else text
    except:
        return text

<<<<<<< HEAD
def language_detection_node(state: State) -> State:
    """STRICT language detection - only en, ur, ar with humanoid responses"""
    original_text = state["text"]
    corrected_text = correct_spelling_and_normalize(original_text)
    state["text"] = corrected_text
    
    def is_latin_script(text):
=======
def language_detection_node(state: TelecoState):
    """STRICT language detection - only en, ur, ar with humanoid responses"""
    # First, correct any spelling errors in the input
    original_text = state["text"]
    corrected_text = correct_spelling_and_normalize(original_text)
    state["text"] = corrected_text  # Update state with corrected text
    
    # Check the SCRIPT being used (not just meaning)
    # If user types in Latin characters, respond in English even if words are Urdu/Arabic
    def is_latin_script(text):
        """Check if text is primarily Latin (English) characters"""
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        latin_chars = sum(1 for c in text if c.isalpha() and ord(c) < 256)
        non_latin_chars = sum(1 for c in text if c.isalpha() and ord(c) >= 256)
        return latin_chars > non_latin_chars
    
    def is_arabic_urdu_script(text):
<<<<<<< HEAD
        arabic_urdu_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F')
        return arabic_urdu_chars > 0
    
    if is_latin_script(corrected_text) and not is_arabic_urdu_script(corrected_text):
        lang = 'en'
    else:
=======
        """Check if text contains Arabic/Urdu script characters"""
        arabic_urdu_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F')
        return arabic_urdu_chars > 0
    
    # If text is in Latin script, treat as English regardless of word meaning
    if is_latin_script(corrected_text) and not is_arabic_urdu_script(corrected_text):
        lang = 'en'
    else:
        # Use LLM for non-Latin script detection
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        prompt = f"""
        STRICTLY detect language of this text based on the SCRIPT used (not the meaning).
        - If it uses Arabic/Urdu script characters, detect as 'ur' for Urdu or 'ar' for Arabic
        - Respond ONLY with exactly one of these codes: 'en', 'ur', or 'ar'
        - If text is in any other language, respond with 'unsupported'
        
        Text: {corrected_text}
        """
        lang = llm.invoke(prompt).content.strip().lower()
    
    if lang not in SUPPORTED_LANGUAGES:
<<<<<<< HEAD
=======
        # Generate humanoid response using LLM instead of hardcoded message
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        humanoid_prompt = f"""
        You are a friendly Teleco customer service assistant. A user has sent a message in a language you don't fully support.
        
        Original message: {original_text}
        
        Generate a warm, friendly, and natural response that:
        1. Acknowledges what they said in a friendly way
        2. Gently explains that you work best with English, Urdu, or Arabic
        3. Invites them to ask their question in one of these languages
        4. Maintains a helpful, conversational tone - NOT robotic
        5. Keep it brief (2-3 sentences max)
        
        DO NOT use phrases like "I cannot" or "I am unable". Be positive and welcoming.
        
        Response in English:
        """
        state["response"] = llm.invoke(humanoid_prompt).content.strip()
<<<<<<< HEAD
        state["should_end"] = True
        state["current_route"] = "reject"
    else:
        state["language"] = lang
        state["original_language"] = lang
        state["current_route"] = "intent_detection"
=======
        state["route"] = "reject"
    else:
        state["language"] = lang
        state["original_language"] = lang
        state["route"] = "intent_detection"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    
    state["agent_path"].append("LanguageDetection")
    return state

<<<<<<< HEAD
def intent_detection_node(state: State) -> State:
=======
def intent_detection_node(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """Detect user intent with STRICT Teleco-only policy"""
    text = state["text"].strip().lower()
    language = state["language"]
    
<<<<<<< HEAD
    english_greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'helo', 'hii', 'heya', 'howdy', 'sup', 'yo', 'hiya']
    english_farewells = ['goodbye', 'bye', 'farewell', 'see you', 'see ya', 'take care', 'good bye', 'fare well', 'byebye', 'bye bye', 'later', 'cya', 'peace', 'cheerio', 'adios', 'goodnight', 'good night', 'gn', 'ttyl']
    
    is_simple_greeting = False
    is_simple_farewell = False
    
    normalized_text = ' '.join(text.split()).lower()
    
    if language == 'en':
        words = normalized_text.split()
        first_words = ' '.join(words[:3]) if len(words) >= 3 else normalized_text
        
        if normalized_text in english_greetings or any(normalized_text.startswith(g) and (len(normalized_text) == len(g) or normalized_text[len(g)] == ' ') for g in english_greetings):
            is_simple_greeting = True
        elif normalized_text in english_farewells or any(normalized_text.startswith(f) and (len(normalized_text) == len(f) or normalized_text[len(f)] == ' ') for f in english_farewells):
            is_simple_farewell = True
=======
    # First, check for simple greetings/farewells directly without LLM
    # Expanded to include common variations and misspellings
    english_greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'helo', 'hii', 'heya', 'howdy', 'sup', 'yo', 'hiya']
    english_farewells = ['goodbye', 'bye', 'farewell', 'see you', 'see ya', 'take care', 'good bye', 'fare well', 'byebye', 'bye bye', 'later', 'cya', 'peace', 'cheerio', 'adios', 'goodnight', 'good night', 'gn', 'ttyl']
    
    # Check if it's a simple greeting
    is_simple_greeting = False
    is_simple_farewell = False
    
    # Normalize text for comparison (remove extra spaces, handle common patterns)
    normalized_text = ' '.join(text.split()).lower()
    
    if language == 'en':
        # Split into words for proper word boundary matching
        words = normalized_text.split()
        first_words = ' '.join(words[:3]) if len(words) >= 3 else normalized_text  # Check first 3 words max
        
        # Check for greetings - must be exact match, start of sentence, or first word
        if normalized_text in english_greetings or any(normalized_text.startswith(g) and (len(normalized_text) == len(g) or normalized_text[len(g)] == ' ') for g in english_greetings):
            is_simple_greeting = True
        # Check for farewells - must be exact match or start of sentence  
        elif normalized_text in english_farewells or any(normalized_text.startswith(f) and (len(normalized_text) == len(f) or normalized_text[len(f)] == ' ') for f in english_farewells):
            is_simple_farewell = True
    
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    elif language == 'ur':
        urdu_greetings = ['ہیلو', 'ہائے', 'سلام', 'السلام علیکم', 'صبح بخیر', 'شام بخیر']
        urdu_farewells = ['الوداع', 'خدا حافظ', 'خدا نگہبان', 'بای', 'پھر ملیں گے']
        if any(greeting in text for greeting in urdu_greetings):
            is_simple_greeting = True
        elif any(farewell in text for farewell in urdu_farewells):
            is_simple_farewell = True
<<<<<<< HEAD
=======
    

>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    elif language == 'ar':
        arabic_greetings = ['مرحبا', 'أهلا', 'سلام', 'صباح الخير', 'مساء الخير']
        arabic_farewells = ['وداعا', 'مع السلامة', 'إلى اللقاء', 'سلام']
        if any(greeting in text for greeting in arabic_greetings):
            is_simple_greeting = True
        elif any(farewell in text for farewell in arabic_farewells):
            is_simple_farewell = True
    
<<<<<<< HEAD
    if is_simple_greeting:
        user_name = state.get("user_name")
        state["response"] = get_random_greeting(language, user_name)
        state["should_end"] = True
        state["is_greeting"] = True
=======
    # Handle simple greetings/farewells immediately
    if is_simple_greeting:
        user_name = state.get("user_name")
        state["response"] = get_random_greeting(language, user_name)
        state["route"] = "greeting_response"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        
        if state.get("is_new_conversation", True):
            state["is_new_conversation"] = False
            
        state["agent_path"].append("IntentDetection")
        return state
    
    if is_simple_farewell:
        user_name = state.get("user_name")
        recent_resolved = False
        conversation_id = state.get("conversation_id")
        if conversation_id and conversation_id in conversation_memory:
            memory = conversation_memory[conversation_id]
            recent_resolved = memory.get("last_issue_resolved", False)
        
        state["response"] = get_random_farewell(language, user_name, recent_resolved)
<<<<<<< HEAD
        state["should_end"] = True
        state["is_farewell"] = True
        
=======
        state["route"] = "farewell_response"
        
        # Clear conversation memory after farewell
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        if conversation_id and conversation_id in conversation_memory:
            del conversation_memory[conversation_id]
            
        state["agent_path"].append("IntentDetection")
        return state
    
<<<<<<< HEAD
    # Use LLM-based detection
    intent, is_teleco_related = detect_intent_and_teleco_relevance(state["text"], state["language"])
    state["previous_intent"] = intent
    
    # Update conversation memory
    conversation_id = state.get("conversation_id")
    if conversation_id and conversation_id in conversation_memory:
        memory = conversation_memory[conversation_id]
=======
    # For more complex cases, use the original LLM-based detection
    # Detect intent AND check Teleco relevance
    intent, is_teleco_related = detect_intent_and_teleco_relevance(state)
    state["previous_intent"] = intent
    
    # Handle conversation memory
    conversation_id = state.get("conversation_id")
    if conversation_id and conversation_id in conversation_memory:
        memory = conversation_memory[conversation_id]
        # Update user name if mentioned
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        if intent == "INTRODUCTION":
            name = extract_user_name(state["text"], state["language"])
            if name:
                memory["user_name"] = name
                state["user_name"] = name
    
<<<<<<< HEAD
    # Handle non-Teleco queries
    if intent == "NON_TELECO_QUERY" or not is_teleco_related:
        response = generate_non_teleco_response(state["language"], state["text"])
        state["response"] = response
        state["should_end"] = True
        state["current_route"] = "non_teleco_response"
=======
    # STRICT: Handle non-Teleco queries immediately
    if intent == "NON_TELECO_QUERY" or not is_teleco_related:
        # Generate polite non-Teleco response
        response = generate_non_teleco_response(state["language"], state["text"])
        state["response"] = response
        state["route"] = "non_teleco_response"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        state["agent_path"].append("IntentDetection")
        return state
    
    # Handle Teleco-related intents
    if intent == "GREETING":
<<<<<<< HEAD
        user_name = state.get("user_name")
        greeting = get_random_greeting(state["language"], user_name)
        state["response"] = greeting
        state["should_end"] = True
        state["is_greeting"] = True
        
        if state.get("is_new_conversation", True):
            state["is_new_conversation"] = False
        state["agent_path"].append("IntentDetection")
        return state
        
    elif intent == "FAREWELL":
=======
        # Generate personalized greeting
        user_name = state.get("user_name")
        greeting = get_random_greeting(state["language"], user_name)
        state["response"] = greeting
        state["route"] = "greeting_response"
        
        # If this is a new conversation, set flag
        if state.get("is_new_conversation", True):
            state["is_new_conversation"] = False
            
    elif intent == "FAREWELL":
        # Check if recent issue was resolved
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        recent_resolved = False
        if conversation_id and conversation_id in conversation_memory:
            memory = conversation_memory[conversation_id]
            recent_resolved = memory.get("last_issue_resolved", False)
        
<<<<<<< HEAD
        user_name = state.get("user_name")
        farewell = get_random_farewell(state["language"], user_name, recent_resolved)
        state["response"] = farewell
        state["should_end"] = True
        state["is_farewell"] = True
        
        if conversation_id and conversation_id in conversation_memory:
            del conversation_memory[conversation_id]
        state["agent_path"].append("IntentDetection")
        return state
        
    elif intent == "THANKS":
=======
        # Generate personalized farewell
        user_name = state.get("user_name")
        farewell = get_random_farewell(state["language"], user_name, recent_resolved)
        state["response"] = farewell
        state["route"] = "farewell_response"
        
        # Clear conversation memory after farewell
        if conversation_id and conversation_id in conversation_memory:
            del conversation_memory[conversation_id]
            
    elif intent == "THANKS":
        # Generate thank you response
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        prompt = f"""
        Generate a warm, professional response to thank you from a Teleco customer.
        
        Language: {state['language']}
        Original message: {state['text']}
        Company: Teleco
        Tone: Appreciative, humble, helpful
        
        Keep it natural and human-like (1-2 sentences).
        
        Response in {state['language']} only:
        """
        response = llm.invoke(prompt).content.strip()
        state["response"] = response
<<<<<<< HEAD
        state["should_end"] = True
        state["agent_path"].append("IntentDetection")
        return state
        
    elif intent == "INTRODUCTION":
        name = extract_user_name(state["text"], state["language"])
        if name:
            state["user_name"] = name
=======
        state["route"] = "thanks_response"
        
    elif intent == "INTRODUCTION":
        # Extract and acknowledge name
        name = extract_user_name(state["text"], state["language"])
        if name:
            state["user_name"] = name
            # Store in memory
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
            if conversation_id:
                if conversation_id not in conversation_memory:
                    conversation_memory[conversation_id] = {}
                conversation_memory[conversation_id]["user_name"] = name
            
<<<<<<< HEAD
=======
            # Generate name acknowledgment
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
            prompt = f"""
            Generate a friendly acknowledgment of the user's name and offer Teleco assistance.
            
            Language: {state['language']}
            User name: {name}
            Company: Teleco
            Tone: Warm, welcoming, professional
            
            Example in English: "Nice to meet you, {name}! I'm here to help with Teleco services. What can I assist you with today?"
            
            Response in {state['language']} only:
            """
            response = llm.invoke(prompt).content.strip()
            state["response"] = response
<<<<<<< HEAD
            state["should_end"] = True
            state["agent_path"].append("IntentDetection")
            return state
    
    state["current_route"] = "translation_node"
    state["agent_path"].append("IntentDetection")
    return state

def translation_node(state: State) -> State:
    """Translate query to English for processing"""
    if state["language"] == 'en':
        state["english_query"] = state["text"]
    else:
        state["english_query"] = translate_to_english(state["text"], state["language"])
    
    state["current_route"] = "teleco_processing"
    state["agent_path"].append("TranslationNode")
    return state

def teleco_processing_node(state: State) -> State:
    """Process Teleco queries through guardrail and router"""
    english_query = state.get("english_query", "")
    
    if not english_query:
        english_query = translate_to_english(state["text"], state["language"])
        state["english_query"] = english_query
    
=======
            state["route"] = "introduction_response"
        else:
            # If no name extracted, continue to Teleco processing
            state["route"] = "translation_node"
            
    elif intent == "TELECO_QUERY" or is_teleco_related:
        # Proceed to translation node first
        state["route"] = "translation_node"
        
    else:
        # Fallback - treat as non-Teleco
        response = generate_non_teleco_response(state["language"], state["text"])
        state["response"] = response
        state["route"] = "non_teleco_response"
    
    state["agent_path"].append("IntentDetection")
    return state

def teleco_processing_node(state: TelecoState):
    """Process Teleco queries through guardrail and router"""
    # Use the English query that was stored in translation_node
    english_query = state.get("english_query", "")
    
    if not english_query:
        # Fallback: translate now if not already done
        english_query = translate_to_english(state["text"], state["language"])
        state["english_query"] = english_query
    
    # Check if query contains Teleco keywords in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    text_lower = english_query.lower()
    english_keywords = SUPPORTED_LANGUAGES['en']
    
    if not any(kw in text_lower for kw in english_keywords):
<<<<<<< HEAD
=======
        # Generate polite Teleco-only response in user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        prompt = f"""
        Politely inform the user that you can only help with Teleco-related queries.
        
        Language: {state['language']}
        
        Requirements:
        - Be polite and helpful
        - Mention you specialize in Teleco services
        - List the areas you can help with (billing, packages, troubleshooting, policies)
        - Keep it friendly (1-2 sentences)
        
        Response in {state['language']} only:
        """
        response = llm.invoke(prompt).content.strip()
        state["response"] = response
<<<<<<< HEAD
        state["should_end"] = True
        state["current_route"] = "reject"
    else:
=======
        state["route"] = "reject"
    else:
        # STRICT: Verify it's about one of the four categories
        # Check if query contains category keywords
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        category_found = False
        for category, cat_keywords in CATEGORY_KEYWORDS.items():
            if any(kw in text_lower for kw in cat_keywords):
                category_found = True
                break
        
        if not category_found:
<<<<<<< HEAD
=======
            # Generate response for non-category Teleco queries in user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
            prompt = f"""
            The user has asked about Teleco but not in one of the specific categories you handle.
            
            Language: {state['language']}
            User query: {state['text']}
            
            Generate a helpful response that:
            1. Acknowledges their Teleco-related query
            2. Politely explains you specialize in specific areas
            3. Lists the areas you can help with (billing, packages, troubleshooting, policies)
            4. Asks if they have questions in these areas
            
            Keep it friendly and helpful (2-3 sentences).
            
            Response in {state['language']} only:
            """
            response = llm.invoke(prompt).content.strip()
            state["response"] = response
<<<<<<< HEAD
            state["should_end"] = True
            state["current_route"] = "reject"
        else:
            state["current_route"] = "router"
=======
            state["route"] = "reject"
        else:
            state["route"] = "router"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    
    state["agent_path"].append("TelecoProcessing")
    return state

<<<<<<< HEAD
def router_node(state: State) -> State:
    """Router - handles five categories including general Teleco queries"""
=======
def router_node(state: TelecoState):
    """Router - handles five categories including general Teleco queries"""
    # Use English query for categorization
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    english_query = state.get("english_query", "")
    if not english_query:
        english_query = translate_to_english(state["text"], state["language"])
    
    prompt = f"""
    Classify this Teleco query into EXACTLY ONE of these FIVE categories:
    - billing: Payments, invoices, fees, charges, bills
    - packages: Plans, data limits, upgrades, pricing, plans
    - troubleshooting: Connection issues, router problems, outages, technical issues
    - policies: Terms, credits, guarantees, SLAs, compensation
    - general: General questions about Teleco, what services they offer, company information, "what is Teleco"
    
    If the query does NOT fit into ANY of these five categories, respond with 'reject'
    
    Query (English): {english_query}
    Category (English only, lowercase):
    """
    category = llm.invoke(prompt).content.strip().lower()
    
<<<<<<< HEAD
    valid_categories = ["billing", "packages", "troubleshooting", "policies", "general"]
    
    if category in valid_categories:
        state["current_route"] = category
        
=======
    # Valid categories now include general
    valid_categories = ["billing", "packages", "troubleshooting", "policies", "general"]
    
    if category in valid_categories:
        state["route"] = category
        
        # Update conversation memory with last category
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        conversation_id = state.get("conversation_id")
        if conversation_id:
            if conversation_id not in conversation_memory:
                conversation_memory[conversation_id] = {}
            conversation_memory[conversation_id]["last_category"] = category
    else:
<<<<<<< HEAD
=======
        # Generate polite rejection response in user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
        prompt = f"""
        Generate a polite response for a Teleco query that doesn't fit your categories.
        
        Language: {state['language']}
        User query: {state['text']}
        
        Response should:
        1. Acknowledge their Teleco query
        2. Politely explain you specialize in specific areas
        3. List the areas you can help with (billing, packages, troubleshooting, policies)
        4. Offer to help with those areas
        
        Keep it friendly (2-3 sentences).
        
        Response in {state['language']} only:
        """
        response = llm.invoke(prompt).content.strip()
        state["response"] = response
<<<<<<< HEAD
        state["should_end"] = True
        state["current_route"] = "reject"
=======
        state["route"] = "reject"
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    
    state["agent_path"].append("Router")
    return state

<<<<<<< HEAD
def rag_retrieve_node(state: State) -> State:
    """Retrieve context from documents using English query"""
=======
def rag_retrieve_node(state: TelecoState):
    """Retrieve context from documents using English query"""
    # Use the English query that was stored in translation_node
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    english_query = state.get("english_query", "")
    if not english_query:
        english_query = translate_to_english(state["text"], state["language"])
    
<<<<<<< HEAD
    context = rag_retrieve(english_query, state["current_route"])
=======
    # Get context using router's category decision
    context = rag_retrieve(english_query, state["route"])
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    
    state["context"] = context
    state["agent_path"].append("RagRetrieve")
    
    print(f"\n{'='*60}")
<<<<<<< HEAD
    print(f"ROUTE: {state['current_route']} | QUERY (EN): {english_query}")
=======
    print(f"ROUTE: {state['route']} | QUERY (EN): {english_query}")
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    print(f"RETRIEVED CONTEXT:\n{context if context else 'NO RELEVANT DOCUMENTS FOUND'}")
    print(f"{'='*60}\n")
    
    return state

<<<<<<< HEAD
def billing_agent(state: State) -> State:
=======
# ===== UPDATED SPECIALIZED AGENTS (ALWAYS WORK IN ENGLISH) =====
def billing_agent(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """Billing specialist - always generates in English, then translates"""
    user_name = state.get("user_name")
    english_query = state.get("english_query", "")
    
<<<<<<< HEAD
=======
    # Generate response in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    You are Teleco's billing specialist. 
    
    Customer name: {user_name if user_name else 'Not provided'}
    
    Context from Teleco documents:
    {state['context']}
    
    User Query (English): {english_query}
    
    Generate a helpful, professional response in English that directly addresses the user's query:
    1. Start with brief acknowledgment
    2. Provide detailed answer with calculations if needed
    3. End with offer for further assistance
    4. Use professional, clear language
    5. DO NOT include any signature, name, or contact information in the response
    6. DO NOT use placeholders like [Your Name] or [Contact Information]
    7. Respond as if you are the chatbot itself, not a human agent
    """
    english_response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Translate response to user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if state["language"] == 'en':
        state["response"] = english_response
    else:
        state["response"] = translate_response(english_response, state["language"])
    
<<<<<<< HEAD
    state["should_end"] = True
    state["agent_path"].append("BillingAgent")
    return state

def packages_agent(state: State) -> State:
=======
    state["agent_path"].append("BillingAgent")
    return state

def packages_agent(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """Packages specialist - always generates in English, then translates"""
    user_name = state.get("user_name")
    english_query = state.get("english_query", "")
    context = state.get('context', '')
    
<<<<<<< HEAD
    has_useful_context = context and len(context.strip()) > 50
    
=======
    # Check if context has useful information
    has_useful_context = context and len(context.strip()) > 50
    
    # Generate response in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    You are Teleco's packages specialist. 
    
    Customer name: {user_name if user_name else 'Not provided'}
    
    === AVAILABLE PACKAGE DOCUMENTATION ===
    {context if has_useful_context else 'NO SPECIFIC DOCUMENTATION FOUND FOR THIS QUERY.'}
    === END OF DOCUMENTATION ===
    
    User Query: {english_query}
    
    CRITICAL INSTRUCTIONS:
    1. If the documentation above contains relevant package information:
       - Acknowledge the query
       - Present options clearly from the documentation
       - Add personalized recommendation if possible
       - End with call to action
    
    2. If NO documentation is available (says "NO SPECIFIC DOCUMENTATION FOUND"):
       - Be HONEST and apologetic
       - Say something like: "I'm sorry, I don't have specific information about [their query] in my knowledge base right now."
       - Suggest contacting Teleco support for detailed package information
       - Mention what types of package queries you CAN help with (data plans, upgrades, pricing)
    
    3. NEVER make up package details or pricing that aren't in the documentation
    4. NEVER give generic advice when you don't have specific info
    5. Sound helpful and professional
    
    DO NOT include any signature or contact information.
    """
    english_response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Translate response to user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if state["language"] == 'en':
        state["response"] = english_response
    else:
        state["response"] = translate_response(english_response, state["language"])
    
<<<<<<< HEAD
    state["should_end"] = True
    state["agent_path"].append("PackagesAgent")
    return state

def troubleshooting_agent(state: State) -> State:
=======
    state["agent_path"].append("PackagesAgent")
    return state

def troubleshooting_agent(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """Troubleshooting specialist - always generates in English, then translates"""
    user_name = state.get("user_name")
    english_query = state.get("english_query", "")
    context = state.get('context', '')
    
<<<<<<< HEAD
    has_useful_context = context and len(context.strip()) > 50
    
=======
    # Check if context has useful information
    has_useful_context = context and len(context.strip()) > 50
    
    # Generate response in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    You are Teleco's troubleshooting specialist. 
    
    Customer name: {user_name if user_name else 'Not provided'}
    
    === AVAILABLE TROUBLESHOOTING DOCUMENTATION ===
    {context if has_useful_context else 'NO SPECIFIC DOCUMENTATION FOUND FOR THIS ISSUE.'}
    === END OF DOCUMENTATION ===
    
    User Issue: {english_query}
    
    CRITICAL INSTRUCTIONS:
    1. If the documentation above contains troubleshooting steps for this issue:
       - Show empathy for their issue
       - Provide the clear troubleshooting steps from the documentation
       - Add next steps if problem persists
       - End with reassurance
    
    2. If NO documentation is available (says "NO SPECIFIC DOCUMENTATION FOUND"):
       - Be HONEST and apologetic
       - Say something like: "I'm sorry, I don't have specific troubleshooting information for [their issue] in my knowledge base right now."
       - Suggest contacting Teleco support for personalized help
       - Mention what types of issues you CAN help with (internet, router, connection issues)
    
    3. NEVER make up troubleshooting steps that aren't in the documentation
    4. NEVER give generic advice when you don't have specific info
    5. Sound warm, empathetic, and helpful
    
    DO NOT include any signature or contact information.
    """
    english_response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Translate response to user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if state["language"] == 'en':
        state["response"] = english_response
    else:
        state["response"] = translate_response(english_response, state["language"])
    
<<<<<<< HEAD
    state["should_end"] = True
    state["agent_path"].append("TroubleshootingAgent")
    
=======
    state["agent_path"].append("TroubleshootingAgent")
    
    # Mark issue as potentially resolved in memory
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    conversation_id = state.get("conversation_id")
    if conversation_id and conversation_id in conversation_memory:
        conversation_memory[conversation_id]["last_issue_resolved"] = True
    
    return state

<<<<<<< HEAD
def policies_agent(state: State) -> State:
=======
def policies_agent(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """Policies specialist - always generates in English, then translates"""
    user_name = state.get("user_name")
    english_query = state.get("english_query", "")
    
<<<<<<< HEAD
=======
    # Generate response in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    You are Teleco's policies specialist. 
    
    Customer name: {user_name if user_name else 'Not provided'}
    
    Context from Teleco documents:
    {state['context']}
    
    User Query (English): {english_query}
    
    Generate a helpful, professional response in English that directly addresses the user's query:
    1. Acknowledge the policy query
    2. Cite relevant policy information
    3. Explain implications clearly
    4. Offer clarification if needed
    5. DO NOT include any signature, name, or contact information in the response
    6. DO NOT use placeholders like [Your Name] or [Contact Information]
    7. Respond as if you are the chatbot itself, not a human agent
    """
    english_response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Translate response to user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if state["language"] == 'en':
        state["response"] = english_response
    else:
        state["response"] = translate_response(english_response, state["language"])
    
<<<<<<< HEAD
    state["should_end"] = True
    state["agent_path"].append("PoliciesAgent")
    return state

def general_agent(state: State) -> State:
=======
    state["agent_path"].append("PoliciesAgent")
    return state

def general_agent(state: TelecoState):
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    """General Teleco information specialist - handles questions about Teleco itself"""
    user_name = state.get("user_name")
    english_query = state.get("english_query", "")
    context = state.get('context', '')
    
<<<<<<< HEAD
    has_useful_context = context and len(context.strip()) > 50
    
=======
    # Check if context is empty or minimal
    has_useful_context = context and len(context.strip()) > 50
    
    # Generate response in English
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    prompt = f"""
    You are Teleco's friendly customer service assistant. The user is asking about Teleco.
    
    Customer name: {user_name if user_name else 'Not provided'}
    
    AVAILABLE INFORMATION FROM DOCUMENTS:
    {context if has_useful_context else 'NO SPECIFIC INFORMATION AVAILABLE FOR THIS QUERY.'}
    
    User Question: {english_query}
    
    CRITICAL RULES:
    1. If the documents above contain the answer to the user's question, provide that answer.
    2. If the documents do NOT contain the specific answer (like founding year, CEO name, company history):
       - Be HONEST and say: "I'm sorry, I don't have specific information about [what they asked] in my knowledge base."
       - Then, mention what you CAN help with (billing, packages, troubleshooting, policies)
    3. NEVER make up information that isn't in the documents.
    4. NEVER give a generic greeting if they asked a specific question.
    5. Sound warm, apologetic, and helpful - like a real person.
    
    Example of good response when you DON'T have the answer:
    "I'm sorry, I don't have that specific information in my knowledge base right now. But I'd be happy to help you with any questions about your bills, service packages, technical issues, or our policies!"
    """
    english_response = llm.invoke(prompt).content.strip()
    
<<<<<<< HEAD
=======
    # Translate response to user's language
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    if state["language"] == 'en':
        state["response"] = english_response
    else:
        state["response"] = translate_response(english_response, state["language"])
    
<<<<<<< HEAD
    state["should_end"] = True
    state["agent_path"].append("GeneralAgent")
    return state

def should_continue(state: State) -> str:
    """Conditional edge function to decide next node"""
    if state.get("should_end", False):
        return "end"
    
    current_route = state.get("current_route", "")
    
    # Define the routing logic
    if current_route == "reject":
        return "end"
    elif current_route == "intent_detection":
        return "intent_detection_node"
    elif current_route == "translation_node":
        return "translation_node"
    elif current_route == "teleco_processing":
        return "teleco_processing_node"
    elif current_route == "router":
        return "router_node"
    elif current_route in ["billing", "packages", "troubleshooting", "policies", "general"]:
        return "rag_retrieve_node"
    else:
        return "end"

def route_after_rag(state: State) -> str:
    """Route to specific agent after RAG retrieval"""
    route = state.get("current_route", "")
    
    if route == "billing":
        return "billing_agent"
    elif route == "packages":
        return "packages_agent"
    elif route == "troubleshooting":
        return "troubleshooting_agent"
    elif route == "policies":
        return "policies_agent"
    elif route == "general":
        return "general_agent"
    else:
        return "end"

def build_workflow():
    """Build the LangGraph workflow"""
    workflow = StateGraph(State)
    
    # Add all nodes
    workflow.add_node("language_detection_node", language_detection_node)
    workflow.add_node("intent_detection_node", intent_detection_node)
    workflow.add_node("translation_node", translation_node)
    workflow.add_node("teleco_processing_node", teleco_processing_node)
    workflow.add_node("router_node", router_node)
    workflow.add_node("rag_retrieve_node", rag_retrieve_node)
    workflow.add_node("billing_agent", billing_agent)
    workflow.add_node("packages_agent", packages_agent)
    workflow.add_node("troubleshooting_agent", troubleshooting_agent)
    workflow.add_node("policies_agent", policies_agent)
    workflow.add_node("general_agent", general_agent)
    
    # Set entry point
    workflow.set_entry_point("language_detection_node")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "language_detection_node",
        should_continue,
        {
            "intent_detection_node": "intent_detection_node",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "intent_detection_node",
        should_continue,
        {
            "translation_node": "translation_node",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "translation_node",
        should_continue,
        {
            "teleco_processing_node": "teleco_processing_node",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "teleco_processing_node",
        should_continue,
        {
            "router_node": "router_node",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "router_node",
        should_continue,
        {
            "rag_retrieve_node": "rag_retrieve_node",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "rag_retrieve_node",
        route_after_rag,
        {
            "billing_agent": "billing_agent",
            "packages_agent": "packages_agent",
            "troubleshooting_agent": "troubleshooting_agent",
            "policies_agent": "policies_agent",
            "general_agent": "general_agent",
            "end": END
        }
    )
    
    # All agent nodes go to end
    workflow.add_edge("billing_agent", END)
    workflow.add_edge("packages_agent", END)
    workflow.add_edge("troubleshooting_agent", END)
    workflow.add_edge("policies_agent", END)
    workflow.add_edge("general_agent", END)
    
    return workflow.compile()

# Create the workflow
workflow = build_workflow()

# ===== MAIN ENTRY POINT =====
=======
    state["agent_path"].append("GeneralAgent")
    return state

>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
def run_agent(query: str, conversation_id: Optional[str] = None) -> HumanoidResponse:
    """
    Main function to run the agent with a given query
    """
<<<<<<< HEAD
    if not conversation_id:
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
    
    is_new_conversation = conversation_id not in conversation_memory
    
    # Check memory for user name
    user_name = None
    if conversation_id in conversation_memory:
        memory = conversation_memory[conversation_id]
        if "user_name" in memory:
            user_name = memory["user_name"]
    
    # Initialize state
    initial_state = State(
        text=query,
        conversation_id=conversation_id,
        is_new_conversation=is_new_conversation,
        language="en",
        original_language="en",
        english_query=None,
        previous_intent=None,
        current_route="",
        agent_path=[],
        context=None,
        user_name=user_name,
        response=None,
        should_end=False,
        is_greeting=False,
        is_farewell=False
    )
    
    # Execute the workflow
    final_state = workflow.invoke(initial_state)
    
    return HumanoidResponse(
        response=final_state["response"] or "I apologize, but I couldn't generate a response.",
        agent_path=final_state["agent_path"],
        language=final_state["language"],
        conversation_id=conversation_id,
        is_greeting=final_state["is_greeting"],
        is_farewell=final_state["is_farewell"]
=======
    # Generate conversation ID if not provided
    if not conversation_id:
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
    
    # Check if this is a new conversation
    is_new_conversation = conversation_id not in conversation_memory
    
    # Initialize state with new field
    state = TelecoState(
        text=query,
        language="en",
        original_language="en",
        route=None,
        agent_path=[],
        response=None,
        context=None,
        conversation_id=conversation_id,
        user_name=None,
        is_new_conversation=is_new_conversation,
        previous_intent=None,
        english_query=None  # New field
    )
    
    # Check memory for user name
    if conversation_id in conversation_memory:
        memory = conversation_memory[conversation_id]
        if "user_name" in memory:
            state["user_name"] = memory["user_name"]
    
    # Execute nodes in sequence
    # Language Detection
    state = language_detection_node(state)
    if state["route"] == "reject":
        return HumanoidResponse(
            response=state["response"],
            agent_path=state["agent_path"],
            language=state["language"],
            conversation_id=conversation_id,
            is_greeting=False,
            is_farewell=False
        )
    
    # Intent Detection (with strict Teleco-only policy)
    state = intent_detection_node(state)
    
    # Check if intent was handled (greeting, farewell, non-Teleco, etc.)
    if state["route"] in ["greeting_response", "farewell_response", 
                         "thanks_response", "introduction_response", 
                         "non_teleco_response"]:
        is_farewell = state["route"] == "farewell_response"
        is_greeting = state["route"] == "greeting_response"
        
        return HumanoidResponse(
            response=state["response"],
            agent_path=state["agent_path"],
            language=state["language"],
            conversation_id=conversation_id,
            is_greeting=is_greeting,
            is_farewell=is_farewell
        )
    
    # Translation Node (for Teleco queries)
    if state["route"] == "translation_node":
        state = translation_node(state)
        state["route"] = "teleco_processing"
    
    # Teleco Processing (only reached for Teleco queries)
    state = teleco_processing_node(state)
    if state["route"] == "reject":
        return HumanoidResponse(
            response=state["response"],
            agent_path=state["agent_path"],
            language=state["language"],
            conversation_id=conversation_id,
            is_greeting=False,
            is_farewell=False
        )
    
    # Router
    state = router_node(state)
    if state["route"] == "reject":
        return HumanoidResponse(
            response=state["response"],
            agent_path=state["agent_path"],
            language=state["language"],
            conversation_id=conversation_id,
            is_greeting=False,
            is_farewell=False
        )
    
    # Rag Retrieve
    state = rag_retrieve_node(state)
    
    # Execute the specialized agent based on route
    if state["route"] == "billing":
        state = billing_agent(state)
    elif state["route"] == "packages":
        state = packages_agent(state)
    elif state["route"] == "troubleshooting":
        state = troubleshooting_agent(state)
    elif state["route"] == "policies":
        state = policies_agent(state)
    elif state["route"] == "general":
        state = general_agent(state)
    
    return HumanoidResponse(
        response=state["response"],
        agent_path=state["agent_path"],
        language=state["language"],
        conversation_id=conversation_id,
        is_greeting=False,
        is_farewell=False
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
    )