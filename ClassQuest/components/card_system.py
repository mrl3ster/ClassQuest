import streamlit as st
import json
from datetime import datetime
from components.pack_animations import animate_pack_opening

def convert_drive_link(url):
    """Convert Google Drive sharing link to direct image link"""
    if 'drive.google.com' in url:
        if '/file/d/' in url:
            file_id = url.split('/file/d/')[1].split('/')[0]
            return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
        elif 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
            return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
    return url

def create_privilege_card(data_manager):
    st.subheader("Create Privilege Card")

    # Add tabs for Create and Manage
    create_tab, manage_tab = st.tabs(["Create New Card", "Manage Existing Cards"])

    with create_tab:
        name = st.text_input("Card Name")
        description = st.text_area("Description")
        st.markdown("""
        ### How to add an image from Google Drive:
        1. Upload your image to Google Drive
        2. Right-click the image and select 'Share'
        3. Make sure 'Anyone with the link' is selected
        4. Copy the share link and paste it below
        5. The link should look like this:
           ```
           https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing
           ```
           For example:
           ```
           https://drive.google.com/file/d/1WIjT251dynXZ40idsxmwTalG-rhc_j-L/view?usp=sharing
           ```
        The system will automatically convert it to the correct display format.
        """)
        image = st.text_input("Card Image URL")
        type = st.selectbox("Card Type", ["Power", "Special", "Bonus", "Challenge"])
        rarity = st.selectbox("Card Rarity", ["Common", "Uncommon", "Rare", "Epic", "Legendary"])
        value = st.number_input("Card Value (Gold)", min_value=0, value=10)

        # Preview section
        if name and description and image:
            st.markdown("### Card Preview")

            if not (image.startswith('http://') or image.startswith('https://')):
                st.error("Please provide a valid image URL starting with http:// or https://")
            else:
                # Convert Google Drive link to direct image link
                image_url = convert_drive_link(image)

                # Show preview
                st.markdown(f"""
                <div style="
                    border: 2px solid #00ff9f;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                    background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                ">
                    <h3 style="color: #00ff9f;">{name}</h3>
                    <span style="color: #ff9100;">Type: {type}</span><br>
                    <span style="color: #ff00e4;">Rarity: {rarity}</span><br>
                    <div style="margin: 10px 0;">
                        <img src="{image_url}" style="max-width: 100%; border-radius: 5px;">
                    </div>
                    <p style="color: #ffffff;">{description}</p>
                    <p style="color: #00f7ff;">Value: {value} gold</p>
                </div>
                """, unsafe_allow_html=True)

                # Create button
                if st.button("Create Card"):
                    try:
                        card_number = data_manager.add_privilege_card(
                            name=name,
                            description=description,
                            image=image_url,
                            type=type,
                            rarity=rarity,
                            value=value
                        )
                        st.success(f"Created privilege card: {name} (#{card_number})")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating card: {str(e)}")

    with manage_tab:
        st.subheader("Manage Existing Cards")
        cards_df = data_manager.get_cards()

        if cards_df.empty:
            st.info("No cards exist yet. Create some cards in the Create New Card tab!")
            return

        # Initialize session state for editing
        if 'editing_card' not in st.session_state:
            st.session_state.editing_card = None

        for _, card in cards_df.iterrows():
            image_url = convert_drive_link(card['image'])
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.session_state.editing_card == card['number']:
                    # Edit form
                    with st.form(f"edit_card_{card['number']}"):
                        edited_name = st.text_input("Name", value=card['name'])
                        edited_description = st.text_area("Description", value=card['description'])
                        edited_image = st.text_input("Image URL", value=card['image'])
                        edited_type = st.selectbox("Type", ["Power", "Special", "Bonus", "Challenge"], index=["Power", "Special", "Bonus", "Challenge"].index(card['type']))
                        edited_rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Epic", "Legendary"], index=["Common", "Uncommon", "Rare", "Epic", "Legendary"].index(card['rarity']))
                        edited_value = st.number_input("Value", min_value=0, value=card['value'])

                        col3, col4 = st.columns(2)
                        with col3:
                            if st.form_submit_button("Save Changes"):
                                success, message = data_manager.update_card(
                                    card['number'],
                                    edited_name,
                                    edited_description,
                                    convert_drive_link(edited_image),
                                    edited_type,
                                    edited_rarity,
                                    edited_value
                                )
                                if success:
                                    st.session_state.editing_card = None
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                        with col4:
                            if st.form_submit_button("Cancel"):
                                st.session_state.editing_card = None
                                st.rerun()
                else:
                    # Display card
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #666;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px;
                        background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                    ">
                        <h3 style="color: #00ff9f;">{card['name']} (#{card['number']})</h3>
                        <span style="color: #ff9100;">Type: {card['type']}</span><br>
                        <span style="color: #ff00e4;">Rarity: {card['rarity']}</span><br>
                        <div style="margin: 10px 0;">
                            <img src="{image_url}" style="max-width: 100%; border-radius: 5px;">
                        </div>
                        <p style="color: #ffffff;">{card['description']}</p>
                        <p style="color: #00f7ff;">Value: {card['value']} gold</p>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                col5, col6 = st.columns(2)
                with col5:
                    if st.button("Edit", key=f"edit_{card['number']}"):
                        st.session_state.editing_card = card['number']
                        st.rerun()
                with col6:
                    if st.button(f"Delete", key=f"delete_{card['number']}"):
                        if st.session_state.get(f'confirm_delete_{card["number"]}', False):
                            success, message = data_manager.delete_card(card['number'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.session_state[f'confirm_delete_{card["number"]}'] = True
                            st.warning(f"Click again to confirm deletion of card #{card['number']}")

def display_student_cards(data_manager, student_name):
    st.subheader("Your Privilege Cards")

    student_data = data_manager.get_student_stats(student_name)
    if student_data:
        cards = json.loads(student_data['cards'])
        equipped_cards = json.loads(student_data['equipped_cards'])
        level = student_data['level']
        max_cards = data_manager.get_max_equippable_cards(level)

        st.info(f"At level {level}, you can equip {max_cards} cards.")

        if not cards:
            st.info("You haven't earned any privilege cards yet!")
            return

        # Display equipped cards first
        if equipped_cards:
            st.markdown("### Equipped Cards")
            cols = st.columns(3)
            for idx, card_number in enumerate(equipped_cards):
                card_data = data_manager.get_card_details(int(card_number))
                image_url = convert_drive_link(card_data[3])  # Convert the image URL
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #00ff9f;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px;
                        background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                    ">
                        <h3 style="color: #00ff9f;">{card_data[1]}</h3>
                        <span style="color: #ff9100;">Type: {card_data[4]}</span><br>
                        <span style="color: #ff00e4;">Rarity: {card_data[5]}</span><br>
                        <div style="margin: 10px 0;">
                            <img src="{image_url}" style="max-width: 100%; border-radius: 5px; width: 200px;">
                        </div>
                        <p style="color: #ffffff;">{card_data[2]}</p>
                        <p style="color: #00f7ff;">Uses: {card_data[7]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Unequip Card #{card_number}", key=f"unequip_{idx}"):
                        success, message = data_manager.unequip_card(student_name, card_number)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

        # Display unequipped cards
        st.markdown("### Available Cards")
        unequipped_cards = [card for card in cards if card not in equipped_cards]
        if unequipped_cards:
            cols = st.columns(3)
            for idx, card_number in enumerate(unequipped_cards):
                card_data = data_manager.get_card_details(int(card_number))
                image_url = convert_drive_link(card_data[3])  # Convert the image URL
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="
                        border: 2px solid #666;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px;
                        background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                    ">
                        <h3 style="color: #00ff9f;">{card_data[1]}</h3>
                        <span style="color: #ff9100;">Type: {card_data[4]}</span><br>
                        <span style="color: #ff00e4;">Rarity: {card_data[5]}</span><br>
                        <div style="margin: 10px 0;">
                            <img src="{image_url}" style="max-width: 100%; border-radius: 5px; width: 200px;">
                        </div>
                        <p style="color: #ffffff;">{card_data[2]}</p>
                        <p style="color: #00f7ff;">Uses: {card_data[7]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if len(equipped_cards) < max_cards:
                        if st.button(f"Equip Card #{card_number}", key=f"equip_{idx}"):
                            success, message = data_manager.equip_card(student_name, card_number)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("Unequip a card first")
        else:
            st.info("All your cards are equipped!")

def display_card_shop(data_manager, student_name):
    st.subheader("Card Shop")

    student_data = data_manager.get_student_stats(student_name)
    if not student_data:
        return

    available_gold = student_data['gold']
    st.write(f"Your Gold: {available_gold}")

    st.markdown("""
    ### Mystery Card Packs
    Discover new cards by opening card packs! Each pack contains a random selection of cards 
    with different rarities. More expensive packs have better chances of rare cards!
    """)

    from utils.constants import CARD_PACKS

    # Display pack options
    for pack_id, pack_info in CARD_PACKS.items():
        can_afford = available_gold >= pack_info['price']

        # Create the drop rates HTML separately
        drop_rates_html = ""
        for rarity, chance in pack_info['probabilities'].items():
            if chance > 0:
                drop_rates_html += f"<span style='color: #ffffff;'>{rarity}: {chance}%</span><br>"

        st.markdown(f"""
        <div style="
            border: 2px solid {'#00ff9f' if can_afford else '#666'};
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
        ">
            <h3 style="color: #00ff9f;">{pack_info['name']}</h3>
            <p style="color: #ffffff;">{pack_info['description']}</p>
            <p style="color: {'#00ff9f' if can_afford else '#ff0000'};">Price: {pack_info['price']} gold</p>
            <div style="margin-top: 10px;">
                <p style="color: #00f7ff;">Drop Rates:</p>
                {drop_rates_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not can_afford:
            st.error(f"Need {pack_info['price'] - available_gold} more gold!")
        else:
            if st.button(f"Purchase {pack_info['name']}", key=f"pack_{pack_id}"):
                success, result = data_manager.purchase_card_pack(student_name, pack_id)
                if success:
                    st.balloons()

                    # Get card details for animation
                    cards_data = [data_manager.get_card_details(int(card_number)) for card_number in result]

                    # Show pack opening animation
                    animation_complete = animate_pack_opening(cards_data)

                    if animation_complete:
                        st.success("Pack opened successfully!")
                        st.rerun()
                else:
                    st.error(result)