import streamlit as st
import random
import io

from groq import Groq

st.set_page_config(page_title="SpeakEasy - Learn with Mr John", page_icon="🗣️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main-header h1 { background: linear-gradient(135deg,#2563eb,#f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; text-align: center; padding: 1rem; }
.chat-msg { padding: 0.75rem 1rem; border-radius: 1rem; margin-bottom: 0.5rem; max-width: 80%; }
.chat-user { background: #2563eb; color: white; margin-left: auto; border-bottom-right-radius: 0.25rem; }
.chat-teacher { background: #f3f4f6; color: #1f2937; margin-right: auto; border-bottom-left-radius: 0.25rem; }
.stat-card { background: white; border-radius: 0.75rem; padding: 1rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.stApp { background: linear-gradient(135deg, #eff6ff 0%, #fefce8 100%); }
</style>
""", unsafe_allow_html=True)

# ===================== TRANSLATIONS =====================
T = {
    "en": {"app":"SpeakEasy","sub":"Learn English with Mr John","class":"Class","chat":"Chat with Mr John","lessons":"Lessons","quizzes":"Quizzes","progress":"My Progress","welcome":"Welcome to SpeakEasy!","greeting":"Hello! I am Mr John. I am your English teacher. What is your name?","type":"Type or speak...","send":"Send","start_quiz":"Start Quiz","submit":"Submit Answers","your_score":"Your Score","out_of":"out of","correct":"Correct","incorrect":"Incorrect","streak":"Day Streak","lessons_done":"Lessons Completed","quizzes_taken":"Quizzes Taken","avg_score":"Average Score","complete":"Complete Lesson","next":"Next Lesson","prev":"Previous Lesson","try_again":"Try Again","back":"Back to Home","reset":"Reset Chat","choose":"Choose a topic to learn","practice":"Practice","examples":"Examples","error_lessons":"No lessons available for this class.","error_quiz":"No quiz available.","no_key":"Groq API key not set. Enter your API key in the sidebar.","settings":"Settings","api_key":"Enter your Groq API Key","name":"Your Name","home":"Home","ask":"Ask Mr John about this topic","answered":"answered","lesson_done":"Lesson Completed!","quiz_done":"Quiz Completed!","all_clear":"All Clear!","voice_tip":"Use the 🎤 microphone below to speak","listen":"Listen","speaking":"Mr John is speaking...","mic_error":"Could not start microphone. Please type instead.","processing_voice":"Processing your voice..."},
    "hi": {"app":"स्पीकईज़ी","sub":"मिस्टर जॉन से अंग्रेज़ी सीखें","class":"कक्षा","chat":"मिस्टर जॉन से बात करें","lessons":"पाठ","quizzes":"प्रश्नोत्तरी","progress":"मेरी प्रगति","welcome":"स्पीकईज़ी में आपका स्वागत है!","greeting":"नमस्ते! मैं मिस्टर जॉन हूँ। आपका नाम क्या है?","type":"बोलें या लिखें...","send":"भेजें","start_quiz":"प्रश्नोत्तरी शुरू करें","submit":"उत्तर जमा करें","your_score":"आपका स्कोर","out_of":"में से","correct":"सही","incorrect":"गलत","streak":"लगातार दिन","lessons_done":"पूरे किए गए पाठ","quizzes_taken":"दी गई प्रश्नोत्तरी","avg_score":"औसत स्कोर","complete":"पाठ पूरा करें","next":"अगला पाठ","prev":"पिछला पाठ","try_again":"फिर से प्रयास करें","back":"होम पर वापस जाएँ","reset":"चैट रीसेट करें","choose":"विषय चुनें","practice":"अभ्यास","examples":"उदाहरण","error_lessons":"कोई पाठ उपलब्ध नहीं।","error_quiz":"कोई प्रश्नोत्तरी नहीं।","no_key":"API कुंजी सेट नहीं है।","settings":"सेटिंग्स","api_key":"API कुंजी दर्ज करें","name":"आपका नाम","home":"होम","ask":"इस विषय के बारे में पूछें","answered":"उत्तर दिए","lesson_done":"पाठ पूरा हुआ!","quiz_done":"प्रश्नोत्तरी पूरी हुई!","all_clear":"सब सही!","voice_tip":"बोलने के लिए 🎤 माइक्रोफ़ोन का उपयोग करें","listen":"सुनें","speaking":"मिस्टर जॉन बोल रहे हैं...","mic_error":"माइक्रोफोन शुरू नहीं हो सका। कृपया टाइप करें।","processing_voice":"आपकी आवाज प्रोसेस हो रही है..."},
    "ta": {"app":"ஸ்பீக் ஈஸி","sub":"திரு ஜானுடன் ஆங்கிலம் கற்கவும்","class":"வகுப்பு","chat":"திரு ஜானுடன் பேசவும்","lessons":"பாடங்கள்","quizzes":"வினாடி வினாக்கள்","progress":"என் முன்னேற்றம்","welcome":"ஸ்பீக் ஈஸிக்கு வரவேற்கிறோம்!","greeting":"வணக்கம்! நான் திரு ஜான். உங்கள் பெயர் என்ன?","type":"பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்...","send":"அனுப்பு","start_quiz":"வினாடி வினாவைத் தொடங்கு","submit":"பதில்களைச் சமர்ப்பிக்கவும்","your_score":"உங்கள் மதிப்பெண்","out_of":"இல்","correct":"சரி","incorrect":"தவறு","streak":"தொடர் நாட்கள்","lessons_done":"முடித்த பாடங்கள்","quizzes_taken":"எடுத்த வினாடி வினாக்கள்","avg_score":"சராசரி மதிப்பெண்","complete":"பாடத்தை முடிக்கவும்","next":"அடுத்த பாடம்","prev":"முந்தைய பாடம்","try_again":"மீண்டும் முயற்சிக்கவும்","back":"முகப்புக்குத் திரும்பு","reset":"அரட்டையை மீட்டமைக்கவும்","choose":"தலைப்பைத் தேர்ந்தெடுக்கவும்","practice":"பயிற்சி","examples":"எடுத்துக்காட்டுகள்","error_lessons":"பாடங்கள் இல்லை.","error_quiz":"வினாடி வினா இல்லை.","no_key":"API விசை அமைக்கப்படவில்லை.","settings":"அமைப்புகள்","api_key":"API விசையை உள்ளிடவும்","name":"உங்கள் பெயர்","home":"முகப்பு","ask":"இந்த தலைப்பைப் பற்றி கேளுங்கள்","answered":"பதிலளித்தார்","lesson_done":"பாடம் முடிந்தது!","quiz_done":"வினாடி வினா முடிந்தது!","all_clear":"அனைத்தும் சரி!","voice_tip":"பேச கீழே உள்ள 🎤 மைக்ரோஃபோனைப் பயன்படுத்தவும்","listen":"கேள்","speaking":"திரு ஜான் பேசுகிறார்...","mic_error":"மைக்ரோஃபோனைத் தொடங்க முடியவில்லை. தயவுசெய்து தட்டச்சு செய்யவும்.","processing_voice":"உங்கள் குரல் செயலாக்கப்படுகிறது..."},
}

# ===================== CURRICULUM =====================
GRADES = {
    1: {"name":"Class 1","lessons":[
        {"id":"g1_l1","topic":"Alphabet A-Z","content":"There are 26 letters in English: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. Vowels: A, E, I, O, U.","examples":["Apple starts with A","Ball starts with B","Cat starts with C"],"practice":"Say the alphabet from A to Z."},
        {"id":"g1_l2","topic":"Phonics Sounds","content":"Each letter makes a sound. A says 'ah', B says 'buh', C says 'cuh' or 'suh'. Practice the sounds of each letter.","examples":["A is for Apple - /a/ /a/ Apple","B is for Ball - /b/ /b/ Ball"],"practice":"Say the sound of letter D."},
        {"id":"g1_l3","topic":"Sight Words","content":"Sight words are common words: a, an, the, I, you, he, she, it, we, they, is, am, are, in, on, at, to, for.","examples":["I am a boy.","She is a girl.","It is a cat."],"practice":"Read: the, and, is, it, in, on."},
        {"id":"g1_l4","topic":"Greetings","content":"Polite words: Good morning, Good afternoon, Good evening, Hello, Hi, Goodbye, See you later.","examples":["Good morning, teacher!","Hello, my name is Rahul.","Goodbye!"],"practice":"Say 'Good morning' to your friend."},
        {"id":"g1_l5","topic":"Numbers 1-20","content":"Count: one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty.","examples":["I have 5 apples.","There are 10 students."],"practice":"Count from 1 to 10."},
        {"id":"g1_l6","topic":"Colors","content":"Primary colors: red, blue, yellow. Other: green, orange, purple, pink, black, white, brown, grey.","examples":["The sky is blue.","Grass is green.","The sun is yellow."],"practice":"What color is your favorite toy?"},
        {"id":"g1_l7","topic":"Animals","content":"Pets: dog, cat, fish, bird. Farm: cow, buffalo, goat, hen, horse. Wild: lion, tiger, elephant, monkey, bear.","examples":["A dog says bow-wow.","A cat says meow.","A cow says moo."],"practice":"Name 3 animals near your home."},
        {"id":"g1_l8","topic":"Body Parts","content":"head, eyes, ears, nose, mouth, teeth, neck, shoulders, arms, hands, fingers, legs, knees, feet, toes.","examples":["I see with my eyes.","I hear with my ears.","I smell with my nose."],"practice":"Point to your nose and ears."},
        {"id":"g1_l9","topic":"My Family","content":"Family: grandfather, grandmother, father, mother, brother, sister, baby.","examples":["My mother cooks food.","My father goes to work.","I love my sister."],"practice":"Say 'This is my family.'"},
        {"id":"g1_l10","topic":"Sentences - This is a...","content":"Describe things: This is a book. This is a pen. This is a table. This is a chair.","examples":["This is a book.","This is a pencil.","This is a bag."],"practice":"Say 'This is a ______' for 3 things."},
    ],"quiz":[
        {"q":"How many letters in English alphabet?","o":["24","26","28","30"],"a":"26"},
        {"q":"Which is a vowel?","o":["B","C","A","D"],"a":"A"},
        {"q":"What do you say in the morning?","o":["Good night","Good morning","Goodbye","Sorry"],"a":"Good morning"},
        {"q":"What color is the sky?","o":["Red","Blue","Green","Yellow"],"a":"Blue"},
        {"q":"A cat says ______","o":["Moo","Bow-wow","Meow","Baa"],"a":"Meow"},
    ]},
    2: {"name":"Class 2","lessons":[
        {"id":"g2_l1","topic":"Opposites","content":"Words with opposite meanings. Big-Small, Hot-Cold, Fast-Slow, Happy-Sad, Tall-Short, Day-Night, Open-Close, Up-Down.","examples":["Elephant is big. Mouse is small.","Coffee is hot. Ice cream is cold."],"practice":"What is opposite of 'happy'?"},
        {"id":"g2_l2","topic":"Plurals","content":"Add 's': cat->cats. Add 'es': bus->buses, dish->dishes, box->boxes. Special: child->children, foot->feet, tooth->teeth.","examples":["One cat, two cats.","One bus, two buses.","One child, two children."],"practice":"What is the plural of 'book'?"},
        {"id":"g2_l3","topic":"Action Words","content":"Verbs: run, jump, eat, sleep, read, write, play, sing, dance, cook, swim, fly, walk, talk, laugh, cry.","examples":["The boy runs fast.","Birds fly in the sky.","She sings a song."],"practice":"Name 3 action words you did today."},
        {"id":"g2_l4","topic":"Question Words","content":"What (thing), Where (place), When (time), Why (reason), Who (person), How (manner).","examples":["What is your name?","Where do you live?","Who is your teacher?"],"practice":"Ask a question using 'What'."},
        {"id":"g2_l5","topic":"Describing Words","content":"Adjectives: big, small, tall, short, long, soft, hard, hot, cold, sweet, sour, beautiful, happy, sad.","examples":["She has a beautiful dress.","The soup is hot.","I have a red ball."],"practice":"Describe your school using 2 words."},
        {"id":"g2_l6","topic":"My School","content":"School: classroom, teacher, desk, chair, blackboard, books, pencils. Subjects: English, Hindi, Maths, Science.","examples":["My school is big.","My teacher is kind.","I love to read books."],"practice":"Tell about your school in 2 sentences."},
        {"id":"g2_l7","topic":"Food and Drinks","content":"Food: rice, bread, chapati, vegetables, fruits, milk, egg, fish, meat. Drinks: water, milk, juice, tea.","examples":["I eat rice and dal for lunch.","I drink milk every morning."],"practice":"What did you eat for breakfast?"},
        {"id":"g2_l8","topic":"Present - I/You/We/They","content":"With I/You/We/They, verb stays the same. I eat, you play, we read, they run.","examples":["I eat breakfast at 7 AM.","You play in the garden.","They go to school."],"practice":"Complete: 'I ___ (drink) milk every day.'"},
        {"id":"g2_l9","topic":"Present - He/She/It","content":"Add 's' or 'es'. He eats, she plays, it runs. For verbs ending in ch,sh,ss,x,o: add 'es'.","examples":["He eats an apple.","She plays the piano.","It rains in July."],"practice":"Complete: 'She ___ (read) a book.'"},
        {"id":"g2_l10","topic":"Prepositions - in, on, under","content":"'In' = inside. 'On' = on top. 'Under' = below.","examples":["Pencil is in the box.","Book is on the table.","Cat is under the chair."],"practice":"Where is your phone? Use in/on/under."},
    ],"quiz":[
        {"q":"Opposite of 'big'?","o":["Tall","Small","Wide","Long"],"a":"Small"},
        {"q":"Plural of 'bus'?","o":["Buses","Busses","Busies","Bus"],"a":"Buses"},
        {"q":"Which is an action word?","o":["Happy","Run","Beautiful","School"],"a":"Run"},
        {"q":"Opposite of 'hot'?","o":["Warm","Cool","Cold","Ice"],"a":"Cold"},
        {"q":"'Book is ___ the table.'","o":["in","on","under","at"],"a":"on"},
    ]},
    3: {"name":"Class 3","lessons":[
        {"id":"g3_l1","topic":"Nouns","content":"Nouns name person, place, animal, or thing. Person: Rahul, teacher. Place: school, Mumbai. Animal: dog, tiger. Thing: book, table.","examples":["Rahul is a student.","The park is beautiful.","The book is on the table."],"practice":"Find 3 nouns in your classroom."},
        {"id":"g3_l2","topic":"Proper & Common Nouns","content":"Common = general (city). Proper = specific, capital letter (Mumbai). Days and months are proper: Monday, January.","examples":["I live in a city. -> I live in Delhi.","He is a boy. -> He is Rahul."],"practice":"Find proper noun: 'The Ganga is a long river.'"},
        {"id":"g3_l3","topic":"Pronouns","content":"I, you, he, she, it, we, they. Me, you, him, her, it, us, them. My, your, his, her, its, our, their.","examples":["Rahul is my friend. He is kind.","I have a book. It is blue."],"practice":"Replace 'Shreya' with pronoun: 'Shreya is dancing.'"},
        {"id":"g3_l4","topic":"Verbs","content":"Action words: eat, drink, run, walk, read, write, speak, listen, cook, draw, paint, climb, throw, catch, help.","examples":["The chef cooks food.","The children draw pictures.","She helps her mother."],"practice":"Find verb: 'The bird flies in the sky.'"},
        {"id":"g3_l5","topic":"Adjectives","content":"Describe nouns: big, small, red, blue, round, square, happy, sad, tall, short, soft, hard, sweet, sour.","examples":["The red apple is sweet.","She has a beautiful smile."],"practice":"Add a describing word: 'The ____ flower is pretty.'"},
        {"id":"g3_l6","topic":"Making Questions","content":"Use question words (What,Where,When,Why,Who,How) or helping verbs (Is,Am,Are,Do,Does).","examples":["You are a student. -> Are you a student?","You like ice cream. -> Do you like ice cream?"],"practice":"Change to question: 'He can swim.'"},
        {"id":"g3_l7","topic":"Reading - The Ant and the Dove","content":"An ant fell in a river. A dove dropped a leaf. The ant climbed on and was saved. Later the ant bit a hunter to save the dove. Moral: One good turn deserves another.","examples":["Who saved the ant? (The dove)","How did the ant save the dove? (Bit the hunter)"],"practice":"What is the moral?"},
        {"id":"g3_l8","topic":"Singular and Plural","content":"Add 's' (book->books), 'es' (box->boxes), y->i+es (baby->babies), f->ves (leaf->leaves), special (child->children, mouse->mice).","examples":["One baby, two babies.","One leaf, two leaves.","One man, two men."],"practice":"Plural of 'tooth'? Plural of 'leaf'?"},
        {"id":"g3_l9","topic":"Gender","content":"Masculine to feminine: boy->girl, king->queen, prince->princess, actor->actress, lion->lioness, tiger->tigress, husband->wife, father->mother, brother->sister.","examples":["The king is kind. The queen is beautiful.","My father is a doctor. My mother is a teacher."],"practice":"Feminine of 'lion'?"},
        {"id":"g3_l10","topic":"Writing - My Best Friend","content":"Write 4-5 sentences: their name, where they sit, what you like, what you play, why special.","examples":["My best friend is Priya. She sits next to me. We play together."],"practice":"Write 3 sentences about your best friend."},
    ],"quiz":[
        {"q":"Which word is a noun?","o":["Beautiful","Run","School","Quickly"],"a":"School"},
        {"q":"Which is a proper noun?","o":["city","dog","Monday","river"],"a":"Monday"},
        {"q":"Replace 'the boy' with pronoun.","o":["She","It","He","They"],"a":"He"},
        {"q":"Find verb: 'The girl sings a song.'","o":["Girl","Sings","Song","The"],"a":"Sings"},
        {"q":"Plural of 'baby'?","o":["Babys","Babies","Babyes","Babiess"],"a":"Babies"},
    ]},
    4: {"name":"Class 4","lessons":[
        {"id":"g4_l1","topic":"Simple Present","content":"Habits and general truths. I/You/We/They + verb. He/She/It + verb+s/es.","examples":["I wake up at 6 AM.","The sun rises in the east.","She reads every day."],"practice":"Complete: 'She ___ (walk) to school.'"},
        {"id":"g4_l2","topic":"Present Continuous","content":"Actions happening NOW. Form: am/is/are + verb+ing.","examples":["I am eating my lunch.","The children are playing.","She is doing homework."],"practice":"What are you doing right now?"},
        {"id":"g4_l3","topic":"Simple Past","content":"Completed actions. Regular: add -ed. Irregular: go->went, eat->ate, see->saw, drink->drank, run->ran, sing->sang, write->wrote.","examples":["I visited my grandmother yesterday.","She went to the market."],"practice":"What did you do yesterday?"},
        {"id":"g4_l4","topic":"Conjunctions","content":"'And' (add), 'But' (contrast), 'Or' (choice).","examples":["I like apples and oranges.","She is small but strong.","Tea or coffee?"],"practice":"Join: 'I like swimming. I like dancing.'"},
        {"id":"g4_l5","topic":"Prepositions of Place","content":"In (inside), On (top), Under (below), Behind (back), In front of (before), Between (middle), Next to (beside), Near (close).","examples":["The cat is behind the door.","My house is between two shops."],"practice":"Where is your school bag?"},
        {"id":"g4_l6","topic":"Prepositions of Time","content":"At (specific time: at 5 PM), In (months/seasons: in July), On (days/dates: on Monday).","examples":["I wake up at 6 AM.","We go on vacation in May.","My birthday is on Jan 10."],"practice":"Complete: 'I was born ___ 2015.'"},
        {"id":"g4_l7","topic":"Paragraph - My Pet","content":"4-5 sentences: pet's name, looks, food, likes, why you love them.","examples":["I have a dog named Tommy. He is brown and white. He loves to play."],"practice":"Write a paragraph about your pet."},
        {"id":"g4_l8","topic":"Reading - The Greedy Dog","content":"A dog with a bone saw his reflection and thought it was another dog with a bigger bone. He barked and lost his bone. Moral: Greed leads to loss.","examples":["What did the dog find? (A bone)","Why did he lose it? (He barked at reflection)"],"practice":"What is the moral?"},
        {"id":"g4_l9","topic":"Synonyms","content":"Words with similar meanings: Big=Large, Happy=Glad, Pretty=Beautiful, Fast=Quick, Smart=Intelligent, Sad=Unhappy, Old=Ancient, Start=Begin.","examples":["The box is big = The box is large.","She is happy = She is glad."],"practice":"Synonym for 'smart'?"},
        {"id":"g4_l10","topic":"Antonyms","content":"Opposites: Hot-Cold, Big-Small, Fast-Slow, Happy-Sad, Rich-Poor, Light-Dark, Full-Empty, Open-Close, Day-Night, Love-Hate.","examples":["Summer is hot. Winter is cold.","I open the door. Then I close it."],"practice":"Antonym of 'rich'?"},
    ],"quiz":[
        {"q":"Complete: 'She ___ to school.'","o":["go","goes","going","went"],"a":"goes"},
        {"q":"'I ___ my lunch right now.'","o":["eat","eats","am eating","ate"],"a":"am eating"},
        {"q":"'Yesterday, I ___ to the park.'","o":["go","goes","going","went"],"a":"went"},
        {"q":"Which shows contrast?","o":["And","But","Or","So"],"a":"But"},
        {"q":"'I was born ___ 2014.'","o":["at","in","on","by"],"a":"in"},
    ]},
    5: {"name":"Class 5","lessons":[
        {"id":"g5_l1","topic":"Articles - A, An, The","content":"'A' before consonant sounds (a book). 'An' before vowel sounds (an apple). 'The' for specific things (the Sun).","examples":["I saw a dog.","I saw an elephant.","The dog I saw was brown."],"practice":"Fill: '___ apple a day...'"},
        {"id":"g5_l2","topic":"Prepositions of Movement","content":"To (towards), From (away), Into (entering), Out of (exiting), Across (side to side), Through (inside), Around (circle), Along (line).","examples":["She walked to school.","The cat jumped into the box.","He ran across the road."],"practice":"'Bird flew ___ the tree.' (across)"},
        {"id":"g5_l3","topic":"Present vs Present Continuous","content":"Simple present = habits. Present continuous = happening now.","examples":["She reads daily (habit).","She is reading now (right now).","Sun rises in east (fact)."],"practice":"'I do/am doing homework right now.'"},
        {"id":"g5_l4","topic":"Past vs Past Continuous","content":"Simple past = completed. Past continuous = in progress. Form: was/were + verb+ing.","examples":["I watched TV yesterday.","I was watching TV when you called."],"practice":"'I ___ (sleep) when doorbell rang.'"},
        {"id":"g5_l5","topic":"Subject-Verb Agreement","content":"Singular -> singular verb (adds s). Plural -> plural verb (no s). Everyone is, Someone is, Nobody is.","examples":["The dog barks. (singular)","The dogs bark. (plural)","Everyone is ready."],"practice":"Correct: 'The children plays.'"},
        {"id":"g5_l6","topic":"Degrees of Comparison","content":"Positive: tall. Comparative: taller. Superlative: tallest. Long words: beautiful -> more beautiful -> most beautiful.","examples":["Rahul is tall.","Rahul is taller than Amit.","Rahul is the tallest."],"practice":"'She is the ___ (smart) girl.'"},
        {"id":"g5_l7","topic":"Writing - Daily Routine","content":"Use simple present. Time words: first, then, after that, finally.","examples":["I wake at 6 AM. First I brush. Then breakfast. I go to school at 8."],"practice":"Describe your daily routine in 5 sentences."},
        {"id":"g5_l8","topic":"Reading - Lion and Mouse","content":"A lion spared a mouse. The mouse later chewed a net to free the lion. Moral: Even small friends can be great helpers.","examples":["Why did lion let mouse go? (Mercy)","How did mouse help? (Chewed net)"],"practice":"What is the moral?"},
        {"id":"g5_l9","topic":"Adverbs","content":"Manner (slowly), Time (now, yesterday), Place (here, there), Frequency (always, never, sometimes).","examples":["She sings beautifully.","I always brush my teeth."],"practice":"Find adverb: 'She walked slowly.'"},
        {"id":"g5_l10","topic":"Letter Writing - Informal","content":"Structure: Address, Date, Salutation (Dear ___), Body, Closing (Your friend/Love), Name.","examples":["Write to your friend about summer vacation."],"practice":"Write a letter to your grandmother thanking her."},
    ],"quiz":[
        {"q":"'___ apple a day...'","o":["A","An","The","None"],"a":"An"},
        {"q":"'I ___ (play) cricket right now.'","o":["play","plays","am playing","played"],"a":"am playing"},
        {"q":"'She is the ___ girl.'","o":["tall","taller","tallest","more tall"],"a":"tallest"},
        {"q":"Find adverb: 'He spoke loudly.'","o":["He","Spoke","Loudly","The"],"a":"Loudly"},
        {"q":"Correct: 'The boys plays football.'","o":["The boys play football.","The boys playing.","The boys played.","The boys are."],"a":"The boys play football."},
    ]},
    6: {"name":"Class 6","lessons":[
        {"id":"g6_l1","topic":"Active and Passive Voice","content":"Active: subject does action. Passive: subject receives action. Simple present passive: is/am/are + V3. Simple past: was/were + V3.","examples":["Active: Cat chased mouse. -> Passive: Mouse was chased by cat."],"practice":"Change to passive: 'The boy broke the window.'"},
        {"id":"g6_l2","topic":"Tenses Overview","content":"Present: Simple, Continuous, Perfect, Perfect Continuous. Past: Simple, Continuous, Perfect, Perfect Continuous. Future: will + base verb.","examples":["I eat (simple present)","I ate (simple past)","I will eat (simple future)"],"practice":"Identify: 'I have been studying for 2 hours.'"},
        {"id":"g6_l3","topic":"Present Perfect","content":"Connects past to present. has/have + past participle. Keywords: just, already, yet, ever, never, for, since.","examples":["I have finished my homework.","Have you ever seen a tiger?"],"practice":"'I ___ (visit) the Taj Mahal twice.'"},
        {"id":"g6_l4","topic":"Reading - The Friendly Mongoose","content":"A mongoose killed a snake to save a baby. Mother saw blood and hit the mongoose, then realized the truth.","examples":["Why was there blood? (Killed snake)","Why did mother hit it? (Thought it hurt baby)"],"practice":"What lesson does this teach?"},
        {"id":"g6_l5","topic":"S-V Agreement - Advanced","content":"Either/or, neither/nor = verb matches nearest subject. Collective nouns: team is (as one). Amounts: Ten rupees is enough.","examples":["Neither teacher nor students were in class.","The committee has decided."],"practice":"Correct: 'Either manager or employees is responsible.'"},
        {"id":"g6_l6","topic":"Conditionals - Type 0 & 1","content":"Type 0 (general truth): If + present, present. Type 1 (real future): If + present, will + verb.","examples":["If you heat ice, it melts. (Type 0)","If it rains, I will stay home. (Type 1)"],"practice":"Type 1: 'If it rains, I ___ (stay) home.'"},
        {"id":"g6_l7","topic":"Writing - Narrative Essay","content":"Tell a story. Structure: Intro (set scene), Body (events in order), Conclusion (what you learned). Past tense.","examples":["Title: My First Day at School","Title: A Memorable Vacation"],"practice":"Write about 'The Best Day of My Life'."},
        {"id":"g6_l8","topic":"Direct & Indirect Speech","content":"Direct: She said, 'I am happy.' Indirect: She said that she was happy. Changes: present->past, will->would, now->then, here->there.","examples":["He said, 'I like ice cream.' -> He said he liked ice cream."],"practice":"Convert: 'Rahul said, \"I am tired.\"'"},
        {"id":"g6_l9","topic":"Phrasal Verbs","content":"get up (wake), look for (search), give up (quit), turn on/off, put on (wear), take off (remove), look after (care), find out (discover).","examples":["Please turn off the lights.","I am looking for my keys."],"practice":"Use 'give up' in a sentence."},
        {"id":"g6_l10","topic":"Idioms","content":"Break the ice (start conversation), Piece of cake (very easy), Under the weather (ill), Let the cat out of the bag (reveal secret).","examples":["The exam was a piece of cake.","I'm under the weather."],"practice":"Use 'break the ice' in a sentence."},
    ],"quiz":[
        {"q":"Passive: 'Cat chased mouse.'","o":["Mouse chased cat.","Mouse was chased by cat.","Mouse is chased.","Mouse chases cat."],"a":"Mouse was chased by cat."},
        {"q":"'I have finished.' = which tense?","o":["Simple past","Present perfect","Past perfect","Present continuous"],"a":"Present perfect"},
        {"q":"'She ___ (visit) the museum twice.'","o":["visited","has visited","had visited","visits"],"a":"has visited"},
        {"q":"Type 1: 'If you study, you ___ pass.'","o":["will","would","can","shall"],"a":"will"},
        {"q":"'Piece of cake' means?","o":["A dessert","Very easy","Very hard","Delicious"],"a":"Very easy"},
    ]},
    7: {"name":"Class 7","lessons":[
        {"id":"g7_l1","topic":"Indirect Speech - Questions","content":"'He asked, \"Where do you live?\"' -> He asked where I lived. Commands: 'She said, \"Sit down.\"' -> She told me to sit down.","examples":["'Are you coming?' -> He asked if I was coming.","'Please help.' -> She requested me to help."],"practice":"'Mother said, \"Clean your room.\"'"},{"id":"g7_l2","topic":"Essay Writing","content":"3 parts: Introduction (hook), Body (3-4 paragraphs), Conclusion (summary). Types: Descriptive, Narrative, Persuasive, Expository.","examples":["Topic: Importance of Education","Topic: My Hobby"],"practice":"Write essay on 'Importance of Reading'."},
        {"id":"g7_l3","topic":"Complex Sentences","content":"Independent clause + dependent clause (because, although, when, while, since, if, unless).","examples":["I stayed home because it rained.","Although tired, she finished homework."],"practice":"Combine: 'I was hungry. I ate lunch.' (because)"},
        {"id":"g7_l4","topic":"Modals","content":"Can (ability), Could (past/polite), May (permission), Might (weak possibility), Should (advice), Must (obligation).","examples":["I can swim.","May I come in?","You must wear seatbelt."],"practice":"Fill: 'You ___ finish homework.' (obligation)"},
        {"id":"g7_l5","topic":"Reading - The Tsunami","content":"2004 tsunami hit India. Tilly Smith saved lives because she learned tsunami signs in geography class.","examples":["How did Tilly save people? (Recognized signs, warned everyone)"],"practice":"Why is geography education important?"},
        {"id":"g7_l6","topic":"Formal Letter","content":"Address, Date, Receiver's address, Subject, Salutation, Body, Closing (Yours faithfully), Name.","examples":["Write to principal for a book fair."],"practice":"Write a formal leave letter to principal."},
        {"id":"g7_l7","topic":"Clauses","content":"Noun clause: 'I know what you did.' Adjective: 'Book that you gave me is great.' Adverb: 'I will call when I reach.'","examples":["What she said surprised everyone. (noun)","The man who helped was kind. (adjective)"],"practice":"Identify clause: 'I know where she lives.'"},
        {"id":"g7_l8","topic":"Report Writing","content":"Headline, Date/Place, Byline, Lead (who,what,when,where,why), Body, Conclusion. Past tense, third person.","examples":["Write a report on Independence Day celebration."],"practice":"Write a report on Annual Sports Day."},
        {"id":"g7_l9","topic":"Figures of Speech","content":"Simile (like/as): 'Sings like a bird.' Metaphor: 'World is a stage.' Personification: 'Wind whispered.' Alliteration: 'Peter Piper.' Onomatopoeia: 'buzz.'","examples":["Simile: Runs like a cheetah.","Metaphor: Time is a thief."],"practice":"Identify: 'Life is like a box of chocolates.'"},
        {"id":"g7_l10","topic":"Debate Skills","content":"For/against a motion. Structure: Greeting, Intro, Arguments with evidence, Conclusion. Formal, respectful tone.","examples":["Topic: Should homework be banned?","Topic: Is social media good?"],"practice":"Prepare arguments FOR/AGAINST mobile phones in school."},
    ],"quiz":[
        {"q":"Indirect: 'Sit down.'","o":["She said sit.","She told me to sit.","She asked sitting.","She told sitting."],"a":"She told me to sit."},
        {"q":"Modal for obligation?","o":["Can","May","Must","Might"],"a":"Must"},
        {"q":"'Life is a journey.' = ?","o":["Simile","Metaphor","Personification","Alliteration"],"a":"Metaphor"},
        {"q":"'You ___ see a doctor.' (advice)","o":["can","might","should","must"],"a":"should"},
        {"q":"'Break the ice' means?","o":["Break ice cubes","Start conversation","End conversation","Freeze water"],"a":"Start conversation"},
    ]},
    8: {"name":"Class 8","lessons":[
        {"id":"g8_l1","topic":"Conditionals - Type 2 & 3","content":"Type 2 (unreal): If + past, would + verb. Type 3 (unreal past): If + past perfect, would have + V3.","examples":["If I were rich, I would travel.","If I had studied, I would have passed."],"practice":"Type 3: 'If I ___ (study), I ___ (pass).'"},
        {"id":"g8_l2","topic":"Passive - All Tenses","content":"Present continuous passive: is/am/are + being + V3. Present perfect passive: has/have + been + V3. Future: will be + V3. Modals: can be, must be.","examples":["She is writing a letter. -> Letter is being written.","They have finished. -> Work has been finished."],"practice":"Passive: 'The chef was cooking dinner.'"},
        {"id":"g8_l3","topic":"Relative Clauses","content":"Who (people), Which (things), That (people/things), Whom (object), Whose (possession), Where (place), When (time).","examples":["Woman who lives next door is teacher.","Book that I read was interesting."],"practice":"Combine: 'I have a friend. She lives in Mumbai.'"},
        {"id":"g8_l4","topic":"Reading - Christmas Present","content":"A letter from a WWI soldier found in an old desk. He wrote about the 1914 Christmas truce when enemies played football together.","examples":["What happened on Christmas 1914? (Truce, played football)"],"practice":"Why was it called 'The Best Christmas Present'?"},
        {"id":"g8_l5","topic":"Determiners","content":"Articles: a,an,the. Demonstratives: this,that,these,those. Possessives: my,your,his,her,its,our,their. Quantifiers: some,any,many,much,few,little,each,every.","examples":["This book is mine.","Some students are absent.","Each child got a gift."],"practice":"Fill: '___ students passed.' (all/many)"},
        {"id":"g8_l6","topic":"Story Writing","content":"Elements: Characters, Setting, Plot (beginning->conflict->climax->resolution), Dialogue, Moral. Past tense, descriptive language.","examples":["Start: 'It was a dark and stormy night...'","Start: 'The old key fit perfectly...'"],"practice":"Write a story from the given starting line."},
        {"id":"g8_l7","topic":"S-V Agreement - Special","content":"'News is good.' (news=singular). 'Mathematics is my favorite.' (subjects=singular). 'Scissors are sharp.' (two parts=plural). 'Ten rupees is enough.' (amounts=singular).","examples":["Politics is not my interest.","The police have arrived."],"practice":"Correct? 'The committee have decided.'"},
        {"id":"g8_l8","topic":"Precis Writing","content":"Summary in 1/3 of original words. Use own words, no opinion, third person, past tense.","examples":["Original -> Precis (summary)"],"practice":"Write a precis of a paragraph from your textbook."},
        {"id":"g8_l9","topic":"Transformation of Sentences","content":"Affirmative->Negative. Assertive->Interrogative. Assertive->Exclamatory. Simple->Complex->Compound.","examples":["He is honest. -> He is not dishonest.","What a beautiful day! -> It is a beautiful day."],"practice":"Transform: 'He is too tired to work.' (so...that)"},
        {"id":"g8_l10","topic":"Dialogue Writing","content":"Natural conversation. New line per speaker. Show emotions through words. Includes greetings and goodbyes.","examples":["Student-teacher dialogue about homework.","Friends discussing exams."],"practice":"Write a dialogue about missing homework."},
    ],"quiz":[
        {"q":"Type 2: 'If I ___ you, I would accept.'","o":["am","was","were","be"],"a":"were"},
        {"q":"Type 3: 'If I knew, I ___ earlier.'","o":["would come","would have come","came","had come"],"a":"would have come"},
        {"q":"Combine: 'I know the girl. She won.'","o":["I know girl she won.","I know girl who won.","I know girl whom won.","I know girl which won."],"a":"I know girl who won."},
        {"q":"'The news ___ good.'","o":["is","are","were","have"],"a":"is"},
        {"q":"'She runs like the wind.' = ?","o":["Simile","Metaphor","Personification","Alliteration"],"a":"Simile"},
    ]},
}

# ===================== AI TEACHER =====================
GRADE_PROMPTS = {
    1: "You are Mr John, a friendly English teacher for Class 1 students (age 6-7). Speak slowly using simple words. Teach alphabet, phonics, sight words, greetings, colors, numbers 1-20, animals. Use encouragement. Keep responses under 3 sentences.",
    2: "You are Mr John, a warm English teacher for Class 2 students (age 7-8). Teach opposite words, plurals, action words, question words. Praise often. Keep responses under 4 sentences.",
    3: "You are Mr John, a supportive English teacher for Class 3 students (age 8-9). Teach nouns, pronouns, verbs, adjectives, questions, short stories. Ask 'what','why','how'. Keep responses under 5 sentences.",
    4: "You are Mr John, an enthusiastic English teacher for Class 4 students (age 9-10). Teach tenses, conjunctions, prepositions, paragraph writing. Keep responses under 5 sentences.",
    5: "You are Mr John, an engaging English teacher for Class 5 students (age 10-11). Teach articles, prepositions, conjunctions, tenses, paragraph writing. Keep responses under 6 sentences.",
    6: "You are Mr John, an insightful English teacher for Class 6 students (age 11-12). Teach passive voice, tenses, comprehension, formal writing. Keep responses under 6 sentences.",
    7: "You are Mr John, a skilled English teacher for Class 7 students (age 12-13). Teach indirect speech, essays, modals, complex sentences. Keep responses under 7 sentences.",
    8: "You are Mr John, an expert English teacher for Class 8 students (age 13-14). Teach advanced grammar, conditionals, letter writing, report writing. Keep responses under 7 sentences.",
}

def ask_mr_john(api_key, grade, message, history, lang="en"):
    if not api_key: return "Please enter your Groq API key in the sidebar to chat with me!"
    client = Groq(api_key=api_key)
    sp = GRADE_PROMPTS.get(grade, GRADE_PROMPTS[1])
    if lang != "en": sp += f" Student's UI is in {lang}. Help with basic {lang} if needed."
    msgs = [{"role":"system","content":sp}]
    for h in history[-10:]: msgs.append({"role":h["role"],"content":h["content"]})
    msgs.append({"role":"user","content":message})
    try:
        r = client.chat.completions.create(model="llama-3.3-70b-versatile",messages=msgs,temperature=0.7,max_tokens=300)
        return r.choices[0].message.content.strip()
    except Exception as e: return f"Sorry: {str(e)}"

def transcribe_audio(audio_bytes, api_key):
    try:
        client = Groq(api_key=api_key)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        r = client.audio.transcriptions.create(model="whisper-large-v3-turbo", file=audio_file)
        return r.text.strip()
    except Exception as e:
        return None

# ===================== TTS JS INJECTION =====================
def inject_tts_js():
    st.markdown("""
<script>
if (!window.__speakEasyInjected) {
    window.__speakEasyInjected = true;
    window.speakText = function(text, lang) {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = lang || 'en-IN';
        u.rate = 0.9;
        u.pitch = 1.05;
        const voices = window.speechSynthesis.getVoices();
        const indianVoice = voices.find(v => v.lang.startsWith('en-IN'));
        if (indianVoice) u.voice = indianVoice;
        window.speechSynthesis.speak(u);
    };
}
</script>
""", unsafe_allow_html=True)


def speak_btn(text):
    t = text.replace("`", "\\`").replace("'", "\\'").replace("\n", " ")
    st.markdown(f'''
<button onclick="speakText('{t}','en-IN')"
    style="background:none;border:1px solid #d1d5db;border-radius:999px;padding:2px 12px;font-size:0.8rem;cursor:pointer;color:#4b5563;transition:all 0.2s"
    onmouseover="this.style.background='#eff6ff';this.style.borderColor='#2563eb';this.style.color='#2563eb'"
    onmouseout="this.style.background='';this.style.borderColor='#d1d5db';this.style.color='#4b5563'">🔊 Listen</button>
''', unsafe_allow_html=True)

# ===================== SESSION STATE =====================
for k in ["name","grade","lang","key","page","chat","done","scores","q_qs","q_as","q_done","l_idx","l_show","voice_input"]:
    if k not in st.session_state:
        if k=="name": st.session_state.name=""
        elif k=="grade": st.session_state.grade=1
        elif k=="lang": st.session_state.lang="en"
        elif k=="key": st.session_state.key=""
        elif k=="page": st.session_state.page="🏠 Home"
        elif k=="chat": st.session_state.chat=[]
        elif k=="done": st.session_state.done=set()
        elif k=="scores": st.session_state.scores=[]
        elif k=="q_qs": st.session_state.q_qs=[]
        elif k=="q_as": st.session_state.q_as={}
        elif k=="q_done": st.session_state.q_done=False
        elif k=="l_idx": st.session_state.l_idx=0
        elif k=="l_show": st.session_state.l_show=False
        elif k=="voice_input": st.session_state.voice_input=""

L = st.session_state.lang
def _(k): return T[L].get(k,T["en"].get(k,k))

# ===================== VOICE JS (injected once) =====================
inject_tts_js()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown(f"### 🗣️ {_('app')}")
    st.markdown(f"*{_('sub')}*")
    st.markdown("---")
    pg = st.radio("",["🏠 Home","💬 Chat","📚 Lessons","🧠 Quizzes","📊 Progress"],
                  index=["🏠 Home","💬 Chat","📚 Lessons","🧠 Quizzes","📊 Progress"].index(st.session_state.page))
    st.session_state.page = pg
    st.markdown("---")
    st.markdown(f"**⚙️ {_('settings')}**")
    k = st.text_input(f"🔑 {_('api_key')}",type="password",value=st.session_state.key,placeholder="gsk_...")
    if k != st.session_state.key: st.session_state.key=k; st.rerun()
    g = st.selectbox(f"📖 {_('class')}",range(1,9),index=st.session_state.grade-1,format_func=lambda x:f"Class {x}")
    if g != st.session_state.grade: st.session_state.grade=g; st.session_state.chat=[]; st.rerun()
    n = st.text_input(f"👤 {_('name')}",value=st.session_state.name)
    if n != st.session_state.name: st.session_state.name=n
    ln = st.selectbox("🌐 Language",["en","hi","ta"],index=["en","hi","ta"].index(L) if L in["en","hi","ta"] else 0,
                      format_func=lambda x:{"en":"English","hi":"हिन्दी","ta":"தமிழ்"}[x])
    if ln != L: st.session_state.lang=ln; st.rerun()
    st.markdown("---")
    st.markdown(f"🔥 {_('streak')}: {len(st.session_state.done)}")
    st.caption(f"💡 {_('voice_tip')}")
    if st.button("🔄 Reset All",use_container_width=True):
        st.session_state.chat=[]
        st.session_state.done=set()
        st.session_state.scores=[]
        st.session_state.q_qs=[]
        st.session_state.q_as={}
        st.session_state.q_done=False
        st.rerun()

# ===================== PAGES =====================
pg = st.session_state.page

# ----- HOME -----
if "Home" in pg:
    st.markdown(f'<div class="main-header"><h1>🗣️ {_("app")}</h1></div>',unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#2563eb">{len(st.session_state.done)}</div><div>📚 {_("lessons_done")}</div></div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#059669">{len(st.session_state.scores)}</div><div>🧠 {_("quizzes_taken")}</div></div>',unsafe_allow_html=True)
    with c3:
        a = round(sum(st.session_state.scores)/len(st.session_state.scores),1) if st.session_state.scores else 0
        st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#d97706">{a}%</div><div>📊 {_("avg_score")}</div></div>',unsafe_allow_html=True)
    with c4:
        ll = len(GRADES[st.session_state.grade]["lessons"])
        st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#7c3aed">{ll}</div><div>📖 {_("lessons")}</div></div>',unsafe_allow_html=True)
    st.markdown("---")
    co1,co2 = st.columns(2)
    with co1:
        if st.button(f"💬 {_('chat')}",use_container_width=True): st.session_state.page="💬 Chat"; st.rerun()
        if st.button(f"🧠 {_('quizzes')}",use_container_width=True): st.session_state.page="🧠 Quizzes"; st.rerun()
    with co2:
        if st.button(f"📚 {_('lessons')}",use_container_width=True): st.session_state.page="📚 Lessons"; st.rerun()
        if st.button(f"📊 {_('progress')}",use_container_width=True): st.session_state.page="📊 Progress"; st.rerun()
    if st.session_state.name:
        st.info(f"👋 Hello **{st.session_state.name}**! You are in **Class {st.session_state.grade}**. {_('voice_tip')}")

# ----- CHAT -----
elif "Chat" in pg:
    st.markdown(f"## 💬 {_('chat')}")
    if not st.session_state.key: st.warning(f"⚠️ {_('no_key')}"); st.stop()

    for m in st.session_state.chat:
        if m["role"]=="user":
            st.markdown(f'<div class="chat-msg chat-user">{m["content"]}</div>',unsafe_allow_html=True)
        else:
            col_msg, col_btn = st.columns([6,1])
            with col_msg:
                st.markdown(f'<div class="chat-msg chat-teacher"><b>👨‍🏫 Mr John:</b> {m["content"]}</div>',unsafe_allow_html=True)
            with col_btn:
                if m["content"] != _("greeting"):
                    speak_btn(m["content"])
    if not st.session_state.chat:
        st.markdown(f'<div class="chat-msg chat-teacher"><b>👨‍🏫 Mr John:</b> {_("greeting")}</div>',unsafe_allow_html=True)
        speak_btn(_("greeting"))

    with st.form("cf",clear_on_submit=True):
        u = st.text_input("",placeholder=_("type"),label_visibility="collapsed")
        if st.form_submit_button(_("send")) and u.strip():
            st.session_state.chat.append({"role":"user","content":u.strip()})
            with st.spinner("👨‍🏫 Mr John is thinking..."):
                r = ask_mr_john(st.session_state.key,st.session_state.grade,u.strip(),st.session_state.chat[:-1],L)
            st.session_state.chat.append({"role":"assistant","content":r})
            st.session_state.voice_input = ""
            st.rerun()

    # Voice recording via st.audio_input
    st.markdown("---")
    audio_val = st.audio_input("🎤 Record your voice message")
    if audio_val is not None:
        with st.spinner(_("processing_voice")):
            audio_bytes = audio_val.getvalue()
            text = transcribe_audio(audio_bytes, st.session_state.key)
        if text:
            st.session_state.chat.append({"role":"user","content":f"🎤 {text}"})
            with st.spinner("👨‍🏫 Mr John is thinking..."):
                r = ask_mr_john(st.session_state.key,st.session_state.grade,text,st.session_state.chat[:-1],L)
            st.session_state.chat.append({"role":"assistant","content":r})
            st.rerun()
        else:
            st.error(_("mic_error"))

    if st.session_state.chat:
        if st.button(f"🗑️ {_('reset')}"): st.session_state.chat=[]; st.rerun()

# ----- LESSONS -----
elif "Lessons" in pg:
    st.markdown(f"## 📚 {_('lessons')} - Class {st.session_state.grade}")
    lessons = GRADES[st.session_state.grade]["lessons"]
    if not lessons: st.info(_("error_lessons")); st.stop()
    cL,cR = st.columns([1,2])
    with cL:
        st.markdown(f"**{_('choose')}**")
        for i,l in enumerate(lessons):
            a = st.session_state.l_idx==i
            if st.button(l["topic"][:20]+("..." if len(l["topic"])>20 else""),key=f"ls_{i}",use_container_width=True,type="primary" if a else "secondary"):
                st.session_state.l_idx=i; st.session_state.l_show=True; st.rerun()
    with cR:
        if not st.session_state.l_show: st.info(f"👈 {_('choose')}")
        else:
            l = lessons[st.session_state.l_idx]
            ok = l["id"] in st.session_state.done
            st.markdown(f"### {'✅ ' if ok else ''}{l['topic']}")
            st.markdown(f"<div style='background:#f8fafc;padding:1rem;border-radius:0.75rem'>{l['content']}</div>",unsafe_allow_html=True)
            if l.get("examples"): st.markdown(f"**📝 {_('examples')}**");[st.markdown(f"- {e}") for e in l["examples"]]
            if l.get("practice"): st.markdown(f"**✏️ {_('practice')}**"); st.info(l["practice"])
            co1,co2,co3 = st.columns(3)
            with co1:
                if st.button(f"◀ {_('prev')}",use_container_width=True) and st.session_state.l_idx>0:
                    st.session_state.l_idx-=1; st.rerun()
            with co2:
                if st.button(f"✅ {_('complete')}",use_container_width=True):
                    st.session_state.done.add(l["id"]); st.success(_("lesson_done")); st.rerun()
            with co3:
                if st.button(f"{_('next')} ▶",use_container_width=True) and st.session_state.l_idx<len(lessons)-1:
                    st.session_state.l_idx+=1; st.rerun()
            if st.session_state.key:
                with st.expander(f"🤖 {_('ask')}"):
                    q = st.text_input("",key="lq")
                    if q:
                        with st.spinner("..."):
                            a = ask_mr_john(st.session_state.key,st.session_state.grade,f"Explain '{l['topic']}'. Student: {q}",[],L)
                        st.markdown(f'<div class="chat-msg chat-teacher"><b>👨‍🏫 Mr John:</b> {a}</div>',unsafe_allow_html=True)
                        speak_btn(a)

# ----- QUIZZES -----
elif "Quizzes" in pg:
    st.markdown(f"## 🧠 {_('quizzes')} - Class {st.session_state.grade}")
    bank = GRADES[st.session_state.grade]["quiz"]
    if not st.session_state.q_qs:
        if st.button(f"🎯 {_('start_quiz')}",use_container_width=True):
            if bank: st.session_state.q_qs=random.sample(bank,min(5,len(bank))); st.session_state.q_as={}; st.session_state.q_done=False; st.rerun()
            else: st.error(_("error_quiz"))
    else:
        if not st.session_state.q_done:
            for i,q in enumerate(st.session_state.q_qs):
                st.markdown(f"**{i+1}. {q['q']}**")
                s = st.radio("",q["o"],key=f"qq_{i}",index=None,label_visibility="collapsed")
                if s: st.session_state.q_as[i]=s
            a = len(st.session_state.q_as); st.progress(a/len(st.session_state.q_qs),text=f"{a}/{len(st.session_state.q_qs)} {_('answered')}")
            if st.button(f"📤 {_('submit')}",use_container_width=True,type="primary"):
                c = sum(1 for i,q in enumerate(st.session_state.q_qs) if st.session_state.q_as.get(i,"").lower()==q["a"].lower())
                p = round(c/len(st.session_state.q_qs)*100,1)
                st.session_state.scores.append(p); st.session_state.q_done=True; st.rerun()
        if st.session_state.q_done:
            c = sum(1 for i,q in enumerate(st.session_state.q_qs) if st.session_state.q_as.get(i,"").lower()==q["a"].lower())
            p = round(c/len(st.session_state.q_qs)*100,1)
            e = "🎉" if p>=80 else "👍" if p>=50 else "💪"
            cl = "#059669" if p>=80 else "#d97706" if p>=50 else "#dc2626"
            st.markdown(f'<div style="text-align:center;padding:1.5rem;background:white;border-radius:1rem;box-shadow:0 1px 3px rgba(0,0,0,0.1)"><div style="font-size:3rem">{e}</div><div style="font-size:1.5rem;font-weight:700;color:{cl}">{_("your_score")}: {c}/{len(st.session_state.q_qs)}</div><div style="font-size:1.25rem;color:#6b7280">{p}%</div></div>',unsafe_allow_html=True)
            for i,q in enumerate(st.session_state.q_qs):
                u = st.session_state.q_as.get(i,"-")
                ok = u.lower()==q["a"].lower()
                st.markdown(f"{'✅' if ok else '❌'} **{i+1}. {q['q']}**  \nYour answer: {u} | Correct: {q['a']}")
            co1,co2 = st.columns(2)
            with co1:
                if st.button(f"🔄 {_('try_again')}",use_container_width=True):
                    st.session_state.q_qs=[]; st.session_state.q_as={}; st.session_state.q_done=False; st.rerun()
            with co2:
                if st.button(f"🏠 {_('back')}",use_container_width=True):
                    st.session_state.page="🏠 Home"; st.session_state.q_qs=[]; st.session_state.q_as={}; st.session_state.q_done=False; st.rerun()

# ----- PROGRESS -----
elif "Progress" in pg:
    st.markdown(f"## 📊 {_('progress')}")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#2563eb">{len(st.session_state.done)}</div><div>📚 {_("lessons_done")}</div></div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#059669">{len(st.session_state.scores)}</div><div>🧠 {_("quizzes_taken")}</div></div>',unsafe_allow_html=True)
    with c3:
        a = round(sum(st.session_state.scores)/len(st.session_state.scores),1) if st.session_state.scores else 0
        st.markdown(f'<div class="stat-card"><div style="font-size:2rem;font-weight:700;color:#d97706">{a}%</div><div>📊 {_("avg_score")}</div></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"### 📚 {_('lessons')}")
    for l in GRADES[st.session_state.grade]["lessons"]:
        st.markdown(f"{'✅' if l['id'] in st.session_state.done else '⬜'} {l['topic']}")
    st.markdown("---")
    if st.session_state.scores:
        st.markdown(f"### 🧠 {_('quizzes')}")
        for i,s in enumerate(st.session_state.scores):
            st.markdown(f"{'🎉' if s>=80 else '👍' if s>=50 else '💪'} Quiz {i+1}: {s}%")
        avg = sum(st.session_state.scores)/len(st.session_state.scores)
        st.progress(avg/100,text=f"{avg:.1f}% {_('avg_score')}")
    else:
        st.info(f"🎯 {_('start_quiz')}")
