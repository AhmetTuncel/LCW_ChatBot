from adaptive_card_example import ADAPTIVE_CARD_CONTENT 


def create_adaptive_card() -> Attachment:
    return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)



async def handle_message(context: TurnContext) -> web.Response:
    # Access the state for the conversation between the user and the bot.
    state = await conversation_state.get(context)
    if hasattr(state, 'in_prompt'):
        if state.in_prompt:
            state.in_prompt = False
            return await card_response(context)
        else:
            state.in_prompt = True
            prompt_message = await create_reply_activity(context.activity, 'Which card would you like to see?\n'
                                                                           '(1) Adaptive Card\n'
                                                                           '(2) Animation Card\n'
                                                                           '(3) Audio Card\n'
                                                                           '(4) Hero Card\n'
                                                                           '(5) Receipt Card\n'
                                                                           '(6) Signin Card\n'
                                                                           '(7) Thumbnail Card\n'
                                                                           '(8) Video Card\n'
                                                                           '(9) All Cards')
            await context.send_activity(prompt_message)
            return web.Response(status=202)
    else:
        state.in_prompt = True
        prompt_message = await create_reply_activity(context.activity, 'Which card would you like to see?\n'
                                                                       '(1) Adaptive Card\n'
                                                                       '(2) Animation Card\n'
                                                                       '(3) Audio Card\n'
                                                                       '(4) Hero Card\n'
                                                                       '(5) Receipt Card\n'
                                                                       '(6) Signin Card\n'
                                                                       '(7) Thumbnail Card\n'
                                                                       '(8) Video Card\n'
                                                                       '(9) All Cards')
        await context.send_activity(prompt_message)
        return web.Response(status=202)


async def card_response(context: TurnContext) -> web.Response:
    response = context.activity.text.strip()
    choice_dict = {
        '1': [create_adaptive_card], 'adaptive card': [create_adaptive_card],
        '2': [create_animation_card], 'animation card': [create_animation_card],
        '3': [create_audio_card], 'audio card': [create_audio_card],
        '4': [create_hero_card], 'hero card': [create_hero_card],
        '5': [create_receipt_card], 'receipt card': [create_receipt_card],
        '6': [create_signin_card], 'signin card': [create_signin_card],
        '7': [create_thumbnail_card], 'thumbnail card': [create_thumbnail_card],
        '8': [create_video_card], 'video card': [create_video_card],
        '9': [create_adaptive_card, create_animation_card, create_audio_card, create_hero_card,
              create_receipt_card, create_signin_card, create_thumbnail_card, create_video_card],
        'all cards': [create_adaptive_card, create_animation_card, create_audio_card, create_hero_card,
                      create_receipt_card, create_signin_card, create_thumbnail_card, create_video_card]
    }

    # Get the functions that will generate the card(s) for our response
    # If the stripped response from the user is not found in our choice_dict, default to None
    choice = choice_dict.get(response, None)
    # If the user's choice was not found, respond saying the bot didn't understand the user's response.
    if not choice:
        not_found = await create_reply_activity(context.activity, 'Sorry, I didn\'t understand that. :(')
        await context.send_activity(not_found)
        return web.Response(status=202)
    else:
        for func in choice:
            card = func()
            response = await create_reply_activity(context.activity, '', card)
            await context.send_activity(response)
        return web.Response(status=200)