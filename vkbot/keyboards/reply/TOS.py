from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

TOSKeyboard = (
    Keyboard(one_time=False, inline=False)
    .add(OpenLink(
        link='https://vk.ru/@extpiar-usloviya-ispolzovaniya-servisa-extautopiar',
        label='📄 Посмотреть ToS'
    ))
    .row()
    .add(Text("✓ Принять"), color=KeyboardButtonColor.POSITIVE)
).get_json()