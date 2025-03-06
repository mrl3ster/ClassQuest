import streamlit as st
import time

def animate_pack_opening(cards_data):
    """
    Display an animated sequence for opening a card pack
    """
    # Pack opening container
    animation_container = st.empty()

    # Initial pack closed state
    animation_container.markdown("""
    <div style="
        width: 200px;
        height: 300px;
        margin: 0 auto;
        background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
        border: 3px solid #00ff9f;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 255, 159, 0.3);
        animation: glow 2s infinite alternate;
    ">
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            color: #00ff9f;
            text-align: center;
            font-family: monospace;
        ">
            Click to Open
        </div>
    </div>
    <style>
    @keyframes glow {
        from {
            box-shadow: 0 0 20px rgba(0, 255, 159, 0.3);
        }
        to {
            box-shadow: 0 0 40px rgba(0, 255, 159, 0.7);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Wait for user click
    if st.button("Open Pack!", key="open_pack_button"):
        # Pack opening animation
        animation_container.markdown("""
        <div style="
            width: 200px;
            height: 300px;
            margin: 0 auto;
            background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
            border: 3px solid #00ff9f;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
            animation: openPack 1s forwards;
        ">
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
                color: #00ff9f;
                text-align: center;
                font-family: monospace;
            ">
                Opening...
            </div>
        </div>
        <style>
        @keyframes openPack {
            0% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.2) rotate(5deg); }
            100% { transform: scale(0) rotate(15deg); }
        }
        </style>
        """, unsafe_allow_html=True)

        time.sleep(1)  # Wait for animation

        # Reveal cards one by one
        for card in cards_data:
            # Get rarity color
            rarity_colors = {
                "Common": "#ffffff",
                "Uncommon": "#00ff9f",
                "Rare": "#00f7ff",
                "Epic": "#b400ff",
                "Legendary": "#ff9100"
            }
            rarity_color = rarity_colors.get(card[5], "#ffffff")

            # Card reveal animation
            animation_container.markdown(f"""
            <div style="
                width: 200px;
                height: 300px;
                margin: 0 auto;
                background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                border: 3px solid {rarity_color};
                border-radius: 15px;
                position: relative;
                overflow: hidden;
                animation: revealCard 0.5s forwards;
            ">
                <div style="padding: 15px; text-align: center;">
                    <h4 style="color: #00ff9f;">{card[1]}</h4>
                    <p style="color: {rarity_color};">{card[5]}</p>
                    <img src="{card[3]}"
                         style="max-width: 100%; border-radius: 5px;">
                </div>
            </div>
            <style>
            @keyframes revealCard {{
                0% {{ transform: scale(0) rotate(-180deg); opacity: 0; }}
                100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
            }}
            </style>
            """, unsafe_allow_html=True)

            time.sleep(0.5)  # Wait between card reveals

        return True

    return False