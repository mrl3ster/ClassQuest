import pandas as pd
import streamlit as st
from utils.constants import DEFAULT_STATS, AVATAR_IMAGES
import hashlib
import json
import psycopg2
from datetime import datetime
import os
import random

class DataManager:
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.load_data()

    def get_db_connection(self):
        return psycopg2.connect(self.db_url)

    def load_data(self):
        try:
            self.students_df = pd.read_csv("students.csv")
            # Add avatar_url column if it doesn't exist or update old image URLs to SVG
            if 'avatar_url' not in self.students_df.columns or 'unsplash.com' in str(self.students_df['avatar_url'].values):
                self.students_df['avatar_url'] = AVATAR_IMAGES[0]  # Set default SVG symbol
            # Add equipped_cards column if it doesn't exist
            if 'equipped_cards' not in self.students_df.columns:
                self.students_df['equipped_cards'] = '[]'
            # Add password column if it doesn't exist
            if 'password_hash' not in self.students_df.columns:
                self.students_df['password_hash'] = ''
        except FileNotFoundError:
            self.students_df = pd.DataFrame(columns=['name', 'gold', 'xp', 'hp', 'level', 'cards', 'avatar_url', 'password_hash', 'equipped_cards'])
            self.save_data()

    def save_data(self):
        self.students_df.to_csv("students.csv", index=False)

    def get_cards(self):
        with self.get_db_connection() as conn:
            return pd.read_sql("SELECT * FROM cards ORDER BY number", conn)

    def add_privilege_card(self, name, description, image, type, rarity, value):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cards (name, description, image, type, rarity, value)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING number
            """, (name, description, image, type, rarity, value))
            conn.commit()
            return cursor.fetchone()[0]

    def update_card_usage(self, card_number):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cards 
                SET usage_count = usage_count + 1,
                    last_used = CURRENT_TIMESTAMP
                WHERE number = %s
            """, (card_number,))
            conn.commit()

    def get_card_details(self, card_number):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cards WHERE number = %s", (card_number,))
            return cursor.fetchone()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_student(self, name, password):
        if name not in self.students_df['name'].values:
            new_student = {
                'name': name,
                **DEFAULT_STATS,
                'cards': '[]',
                'equipped_cards': '[]',
                'password_hash': self.hash_password(password)
            }
            self.students_df = pd.concat([self.students_df, pd.DataFrame([new_student])], ignore_index=True)
            self.save_data()
            return True
        return False

    def verify_student_password(self, name, password):
        if name in self.students_df['name'].values:
            student = self.students_df[self.students_df['name'] == name].iloc[0]
            return student['password_hash'] == self.hash_password(password)
        return False

    def update_student_stats(self, name, stat, value):
        if name in self.students_df['name'].values:
            self.students_df.loc[self.students_df['name'] == name, stat] = value
            self.save_data()
            return True
        return False

    def get_student_stats(self, name):
        if name in self.students_df['name'].values:
            return self.students_df[self.students_df['name'] == name].iloc[0].to_dict()
        return None

    def get_max_equippable_cards(self, level):
        if level >= 10:
            return 3
        elif level >= 5:
            return 2
        else:
            return 1

    def equip_card(self, student_name, card_number):
        student_data = self.get_student_stats(student_name)
        if not student_data:
            return False, "Student not found"

        equipped_cards = json.loads(student_data['equipped_cards'])
        owned_cards = json.loads(student_data['cards'])

        if str(card_number) not in owned_cards:
            return False, "You don't own this card"

        max_cards = self.get_max_equippable_cards(student_data['level'])

        if str(card_number) in equipped_cards:
            return False, "Card already equipped"

        if len(equipped_cards) >= max_cards:
            return False, f"You can only equip {max_cards} cards at level {student_data['level']}"

        equipped_cards.append(str(card_number))
        self.update_student_stats(student_name, 'equipped_cards', json.dumps(equipped_cards))
        self.update_card_usage(card_number)
        return True, "Card equipped successfully"

    def unequip_card(self, student_name, card_number):
        student_data = self.get_student_stats(student_name)
        if not student_data:
            return False, "Student not found"

        equipped_cards = json.loads(student_data['equipped_cards'])

        if str(card_number) not in equipped_cards:
            return False, "Card not equipped"

        equipped_cards.remove(str(card_number))
        self.update_student_stats(student_name, 'equipped_cards', json.dumps(equipped_cards))
        return True, "Card unequipped successfully"

    def delete_card(self, card_number):
        """Delete a card from the database"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                # First check if the card exists
                cursor.execute("SELECT name FROM cards WHERE number = %s", (card_number,))
                card = cursor.fetchone()
                if not card:
                    return False, "Card not found"

                # Delete the card
                cursor.execute("DELETE FROM cards WHERE number = %s", (card_number,))
                conn.commit()

                # Remove the card from all students who have it
                for _, student in self.students_df.iterrows():
                    cards = json.loads(student['cards'])
                    equipped_cards = json.loads(student['equipped_cards'])

                    if str(card_number) in cards:
                        cards.remove(str(card_number))
                        self.update_student_stats(student['name'], 'cards', json.dumps(cards))

                    if str(card_number) in equipped_cards:
                        equipped_cards.remove(str(card_number))
                        self.update_student_stats(student['name'], 'equipped_cards', json.dumps(equipped_cards))

                return True, f"Card #{card_number} ({card[0]}) has been deleted"
        except Exception as e:
            return False, f"Error deleting card: {str(e)}"

    def update_card(self, card_number, name, description, image, type, rarity, value):
        """Update an existing card's details"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cards 
                    SET name = %s, description = %s, image = %s, 
                        type = %s, rarity = %s, value = %s
                    WHERE number = %s
                    RETURNING number
                """, (name, description, image, type, rarity, value, card_number))
                conn.commit()
                if cursor.rowcount == 0:
                    return False, "Card not found"
                return True, f"Card #{card_number} updated successfully"
        except Exception as e:
            return False, f"Error updating card: {str(e)}"

    def get_random_card_by_rarity(self, rarity):
        """Get a random card of specific rarity"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT number FROM cards WHERE rarity = %s", (rarity,))
            cards = cursor.fetchall()
            if cards:
                return random.choice(cards)[0]
            return None

    def generate_pack_cards(self, pack_type):
        """Generate cards for a pack based on probabilities"""
        from utils.constants import CARD_PACKS
        pack_info = CARD_PACKS[pack_type]
        cards = []

        # Handle guaranteed cards first
        if "guaranteed" in pack_info:
            for rarity in pack_info["guaranteed"]:
                card = self.get_random_card_by_rarity(rarity)
                if card:
                    cards.append(str(card))
                    if len(cards) >= pack_info["cards_per_pack"]:
                        return cards

        # Fill remaining slots
        remaining_slots = pack_info["cards_per_pack"] - len(cards)
        probabilities = pack_info["probabilities"]

        for _ in range(remaining_slots):
            roll = random.randint(1, 100)
            cumulative = 0
            selected_rarity = None

            for rarity, chance in probabilities.items():
                cumulative += chance
                if roll <= cumulative:
                    selected_rarity = rarity
                    break

            if selected_rarity:
                card = self.get_random_card_by_rarity(selected_rarity)
                if card:
                    cards.append(str(card))

        return cards

    def purchase_card_pack(self, student_name, pack_type):
        """Purchase and open a card pack"""
        from utils.constants import CARD_PACKS

        if pack_type not in CARD_PACKS:
            return False, "Invalid pack type"

        pack_info = CARD_PACKS[pack_type]
        student_data = self.get_student_stats(student_name)

        if not student_data:
            return False, "Student not found"

        if student_data['gold'] < pack_info['price']:
            return False, f"Not enough gold. Need {pack_info['price']} gold"

        # Generate cards from pack
        new_cards = self.generate_pack_cards(pack_type)
        if not new_cards:
            return False, "Failed to generate cards"

        # Add cards to student's collection
        current_cards = json.loads(student_data['cards'])
        current_cards.extend(new_cards)

        # Update student's gold and cards
        self.update_student_stats(student_name, 'gold', student_data['gold'] - pack_info['price'])
        self.update_student_stats(student_name, 'cards', json.dumps(current_cards))

        return True, new_cards