from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def save_data(new_question):
    session.add(new_question)
    session.commit()


flashcards = session.query(Flashcard).all()


def show_main_menu():
    while True:
        main_command = input("""1. Add flashcards
2. Practice flashcards
3. Exit\n""")
        if main_command == "1":
            show_add_menu()
        elif main_command == "2":
            practise_flashcards()
        elif main_command == "3":
            print("\nBye!")
            exit()
        else:
            print(f'{main_command} is not an option')


def show_add_menu():
    while True:
        command = input("""1. Add a new flashcard
2. Exit\n""")
        if command == "1":
            add_new_flashcard()
        elif command == "2":
            break
        else:
            print(f'{command} is not an option')


def practise_flashcards():
    if len(flashcards) == 0:
        print("There is no flashcard to practice!\n")
    else:
        for flashcard in flashcards:
            print(f'Question: {flashcard.question}')
            while True:
                command = input("""press "y" to see the answer:
press "n" to skip:
press "u" to update:\n""")
                if command == "y":
                    print(f'Answer: {flashcard.answer}\n')
                    break
                elif command == "n":
                    break
                elif command == "u":
                    update_menu(flashcard)
                    break
                else:
                    print(f'{command} is not an option\n')


def add_new_flashcard():
    while True:
        question = input("Question:\n")
        if question == '':
            print("Question can't be empty")
            continue
        break
    while True:
        answer = input("Answer:\n")
        if answer == '':
            print("Answer can't be empty")
            continue
        break

    save_data(Flashcard(question=question, answer=answer))
    flashcards.clear()
    flashcards.extend(session.query(Flashcard).all())


def update_menu(flashcard):
    while True:
        command = input("""press "d" to delete the flashcard:
press "e" to edit the flashcard:\n""")
        if command == "d":
            delete_flashcard(flashcard)
            break
        elif command == "e":
            edit_flashcard(flashcard)
            break
        else:
            print(f"{command} is not an option")
            continue


def delete_flashcard(flashcard):
    session.delete(flashcard)
    session.commit()


def edit_flashcard(flashcard):
    print(f"\ncurrent question: {flashcard.question}")
    new_question = input("please write a new question:\n") or flashcard.question

    print(f"\ncurrent answer: {flashcard.answer}")
    new_answer = input("please write a new answer:\n") or flashcard.answer

    entries = session.query(Flashcard).all()

    for i in entries:
        if i.question == flashcard.question:
            i.answer = new_answer
            i.question = new_question
            session.commit()


show_main_menu()
