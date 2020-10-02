# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:05:52 2019

@author: ses71
"""

def main():
    input("This is a game that quizzes your grammar to guess your language family. \nReady?")
    input("Please answer in complete sentences." "\nAt any time, enter 'quit' to end this program.")

        
        
    import nltk 
    from nltk.corpus import wordnet #used to isolate lemmas
    from nltk.stem import WordNetLemmatizer
    from nltk import word_tokenize, pos_tag, FreqDist 
    from collections import defaultdict
    
    ans_errors=defaultdict(list)
    lemmatizer=WordNetLemmatizer()
    
    test_answer=[]
    test_store=[]
    test_store2=[]
    test_store3=[]
    
    #These are the language families we're testing
    Romance={"language":"Romance","score":0, "test":"modals", "test2":"prepositions", "test3":"negation"} #how do you call/how is the word
    Asian={"language":"Asian","score":0, "test":"modals", "test2":("suffixes","plurality", "prepositions"), "test3":"tense"}
    Slavic={"language":"Slavic","score":0, "test":("modals", "omitted"), "test2":("suffixes", "prepositions")} #"old" con
    Indo_Aryan={"language":"Indo_Aryan","score":0, "test":"omitted", "test2": "prepositions", "test3": ("quantifiers", "reflexives")}
    Germanic={"language":"Germanic","score":0, "test":"modals", "test2": "suffixes", "test3": "S/Ouse"}
    
    #These are the first round of questions we're asking
    
    questions={"S1Q1": "How old are you?", "S1Q2": "If you don't remember a specific word or phrase in English, tell us the question you would ask someone for help.",
               "S1Q3": "How long have you studied English?", "S1Q4": "How often do you see your friends?",
               "S1Q5": "Where do you go grocery shopping?"}
    answer_key=[("I am 32 years old.", "I'm 30 years old."), ("How do you say?", "What is it called?"), "I have studied English for 8 years.", "I see them several times a week.", "I go grocery shopping at the store."]
    
    def isolate_lemmas():#tests for presence of modals based on its lemma
        def get_wordnet_pos(word):
            tag=nltk.pos_tag([word])[0][1][0].upper() #nltk pos_tagger lists tags in three letter acronyms, those need to be matched with wordnet's tagger
            tag_dict={"J": wordnet.ADJ,
                      "N": wordnet.NOUN,
                      "V": wordnet.VERB,
                      "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)
        for user, answer in zip(test_store, test_answer): 
            user=test_store.copy()
            user=' '.join(user)
            answer=test_answer.copy()
            answer=','.join(map(str, answer))
        user=[lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(user)]
        answer=[lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(answer)]
        #diff=[w for w in user and answer if w.isalpha() and (w not in user or w not in answer)]
        return user #checks for same content
     
           
    def modals(): #directly checks for these modals listed, there are definitely more but this is expressly for these purposes
        lemmas=isolate_lemmas()
        modals= ["can", "could", "able", "may", "might", "must", "need", "ought", "have" ]
        for modal in modals:
            if modal in lemmas:
                mistakes1()
            else:
                pass
             
    sig_sf=[] #these empty lists will isolate all word endings with the intention of getting all suffixes
    db_sf=[]
    trp_sf=[]
    
    def suffixes(): #identifies list of acceptable suffixes and compares them
        for user, accept in zip(test_store, answer_key):
            user=identify_suffixes(test_store)
            accept=identify_suffixes(answer_key)
            diff=[w for w in user and accept if w not in user or w not in accept]
            if len(diff) > 0:
                mistakes2()
           
    
    def identify_suffixes(test_list): #create suffix list
        for answer in test_list:
            answer=test_list.copy()
            answer=','.join(map(str, answer))
            #cont=re.findall("\'\w+", answer) #eliminate contractions (I couldn't get this to work)
            answer=word_tokenize(answer)
            answer=[w.lower() for w in answer if w.isalpha()]
        
        for w in answer:
            sig_sf.append(w[-1:])#gets freq dist of suffixes in correct answers
            db_sf.append(w[-2:])
            trp_sf.append(w[-3:])
            
        affixes=sig_sf+db_sf+trp_sf
        suffixes=set(affixes)
        return suffixes
    
    
    figure=[]
    def record_answers(): #call function to save user input; this is where we'll start
        for question, answer in zip(questions.values(), answer_key):
            user_answer=input(question)
            test_store.append(user_answer)
            test_answer.append(answer)
            if user_answer == "quit":
                break
            else:
                for num in questions.keys(): #this for loop actually calls each grammar function- the problem is that it calls each function multiple times [i.e. 1, then 1,2, then 1,2,3, etc]
                    figure.append(num)
                for num in figure:
                    functiontoCall=ans_errors[num]
                    
                    functiontoCall()                
        first_guess()
    
        
    ans_errors={"S1Q1": modals, "S1Q2": modals, "S1Q3": suffixes, "S1Q4": suffixes, "S1Q5": suffixes} #functioncall assigned by question #
            
    #def gram_eval(): #call functions to evaluate errors
     #   for answer in ans_errors.values():
      #      print(answer)
    
    languages=[Romance, Slavic, Indo_Aryan, Germanic, Asian]
            #tell me the diff between test_store and answer key
    
    def mistakes1(): # to assign points to languages with only modals and omitted; omitted function doesn't exist
        for language in languages:
            if language["test"] == "modals":
                language["score"] +=1
            elif language["test"] == "omitted":
                language["score"] +=1
            else:
                continue
    
    def mistakes2():
        for language in languages: #to assign points to languages with only suffixes and prepositions; prepositions function doesn't exist
            if language["test2"] == "suffixes":
                language["score"] +=1
            elif language["test2"] == "prepositions":
                language["score"] +=1
            else:
                continue
                
                
    questions2=("\na. They gave me advices. \nb. They gave me some advice. \nc. They gave me advice.", "\na.Explain me how to do it. \nb.Explain to me how to do it. \nc.Explain how to do it.", "\na. If it will snow tomorrow, we will stay home. \nb.If it snows tomorrow, we will stay home.",
            "\na. We did a mistake. \nb. We are a mistake. \nc. We made a mistake.", "\na. He got a job in Microsoft. \nb. He got a job at Microsoft.") #not a fan of this section -JM
    
    murica=[("'They gave me some advice'. or  'They gave me advice.'"), ("'Explain to me how to do it.' or  'Explain how to do it.'"), "If it snows tomorrow, we will stay home.", ("'We are a mistake.' or 'We made a mistake.'"), "He got a job at Microsoft." ]

    
    
    #fix FOE multi -jumps to mistakes 2 without running program
    
    def multiQ():
        print("For the following section, enter the letter that sounds the best.") #it was by coincidence that all of these were a's. Next time will isolate each letter to return to the user
        input()
        for question in questions2:
            user_answer=input(question).lower()
            test_store2.append(user_answer)
            if user_answer == 'a':
                mistakes1()
                mistakes2()
            else:
                continue               
        second_guess()
                    
    high_score=[]               #evaluates the scoring system and counts points, in order avoid guessing twice on a language, the language is removed in the guesses 
    def scoring(): 
        for language in languages:
            high_score.append(language["score"])
            winner=max(high_score)
        for language in languages:
            if language["score"] == winner:
                return language["language"], languages.index(language)
            else:
                continue
                 
    murica=[("'They gave me some advice'. or  'They gave me advice.'"), ("'Explain to me how to do it.' or  'Explain how to do it.'"), "If it snows tomorrow, we will stay home.", ("'We are a mistake.' or 'We made a mistake.'"), "He got a job at Microsoft." ]
    
    def first_guess():#call function after q5
            for answer, user in zip(answer_key, test_store):
                print("A typical American English speaker would say: ", answer)
                print("You answered:", user)
                input()
            print("Based on these answers: ")
            family=scoring()
            print("Is your language in this language family?", family[0])
            answer=input("Type 'yes' or 'no'. ").lower()
            if answer == "no":
                languages.pop(0)
                answer2=input("Would you like to answer more questions? \nAnswer 'yes' or 'no'. \nEnter 'quit' to end this program. " ).lower()
                if answer2 == "yes":
                    print(answer2)
                    multiQ()
                else:
                    exit()    
    
    def second_guess():#call function after q10
            for us_ans, answer  in zip(test_store2, murica):
                print("A typical American English speaker would say: ", answer)
                print("You answered:", us_ans)
                input()
            print("Based on these answers: ")
            family=scoring()
            print("Is your language in this language family?", family[0])#indexing values for easy popping
            
            answer=input("Type 'yes' or 'no'.").lower()
            
            if answer == "no":
                languages.pop(0)
                answer2=input("Would you like to answer more questions? \nAnswer 'yes' or 'no'. \nEnter 'quit' to end this program. " ).lower()
                if answer2 == "yes":
                    print(answer2)
                    fitb()
                else:
                    exit()
    
    fitb_ans=[("learned", "taught"), ("more", "much"), ("work", "working"), ("nothing", "anything"), ("run", "ran")]
    ans_key=["taught", "much", "working", "anything", "ran"]
    questions3="I {} you how to swim.", "You're {} better than me.", "I enjoy {} with you.", "They don't like {}.", "Last week, I {}."
    
    
    def fitb():#this section is more pretty than functional 
        print("For the following section, please fill in the blank with the given prompts.")
        input()
        for question, answer in zip(questions3, fitb_ans):
            print(question, answer)
            print(question.format(input()))
            user=input()
            test_store3.append(user)
        for user, answer in zip(test_store3, ans_key):  
            if user == answer:
                pass
            elif user.endswith('ing'):
                mistakes2()
            else:
                mistakes1()
        
        third_guess()
    
    def third_guess():
        for answer, user in zip(ans_key, test_store3):
            print("A typical American English speaker would say: ", answer)
            print("You answered:", user)
            input()
            family=scoring()
            print("Based on these answers: ", family[0])
            answer=input("Is your language in this language family?" "\nType 'yes' or 'no'.", family).lower()
            if answer == "yes":
                print("Thank you for participating!")
                exit()
            elif answer == "no":
                answer2= input("Is your native langauge English? " "\nType 'yes' or 'no'.").lower()
                if answer2 == "no":
                    print("We do not have enough information to determine your language family.")
                else:
                    print("ConGratUlations, You sPeAk EnGliSH.")
                    exit()
    
    record_answers()

        
main()  
  
restart=input("Do you want to retake the quiz?") #option to rerun it

if restart == "yes":
    main()    
else:
    exit()     