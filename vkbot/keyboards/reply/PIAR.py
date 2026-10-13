from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

TOSKeyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("⏳ Подать заявку на пиар"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("❗ Обратиться в поддержку"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(OpenLink(
        link='https://github.com/grationz720-dotcom/EXTAutopiar',
        label='📄 Посмотреть код'
    ))
).get_json()