
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

ADMIN_LOGIN_CMD = "adminkentkplaytokenpydroid"
ADMIN_PASSWORD = "63580"

admin_state = {}

def register_admin(dp, bot, OWNER_ID, add_balance, get_balance, balances, CURRENCY):

    def back_kb():
        kb = InlineKeyboardBuilder()
        kb.button(text="← Назад", callback_data="adm_back")
        return kb.as_markup()

    def main_kb():
        kb = InlineKeyboardBuilder()
        kb.button(text="💸 Выдать", callback_data="adm_give")
        kb.button(text="➖ Снять", callback_data="adm_take")
        kb.button(text="💰 Баланс", callback_data="adm_bal")
        kb.adjust(2)
        return kb.as_markup()

    @dp.message(lambda m: m.text == ADMIN_LOGIN_CMD)
    async def admin_login(msg: types.Message):
        if msg.from_user.id != OWNER_ID:
            return
        admin_state[msg.from_user.id] = {"step": "password"}
        await msg.reply("🔐 Пароль?")

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "password")
    async def admin_password(msg: types.Message):
        if msg.text != ADMIN_PASSWORD:
            await msg.reply("❌ Неверно")
            return
        admin_state[msg.from_user.id] = {}
        await msg.reply("🛡 Админ-панель", reply_markup=main_kb())

    @dp.callback_query(lambda c: c.data == "adm_back")
    async def adm_back(call: types.CallbackQuery):
        await call.message.edit_text("🛡 Админ-панель", reply_markup=main_kb())

    @dp.callback_query(lambda c: c.data == "adm_give")
    async def adm_give(call: types.CallbackQuery):
        admin_state[call.from_user.id] = {"step": "give_id"}
        await call.message.edit_text("🆔 Айди?", reply_markup=back_kb())

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "give_id")
    async def give_id(msg: types.Message):
        if not msg.text.isdigit():
            return
        admin_state[msg.from_user.id] = {"step": "give_sum", "target": int(msg.text)}
        await msg.reply("💰 Сумма?")

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "give_sum")
    async def give_sum(msg: types.Message):
        if not msg.text.isdigit():
            return
        uid = admin_state[msg.from_user.id]["target"]
        add_balance(uid, int(msg.text))
        admin_state[msg.from_user.id] = {}
        await msg.reply("✅ Успешно", reply_markup=main_kb())

    @dp.callback_query(lambda c: c.data == "adm_take")
    async def adm_take(call: types.CallbackQuery):
        admin_state[call.from_user.id] = {"step": "take_id"}
        await call.message.edit_text("🆔 Айди?", reply_markup=back_kb())

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "take_id")
    async def take_id(msg: types.Message):
        if not msg.text.isdigit():
            return
        admin_state[msg.from_user.id] = {"step": "take_sum", "target": int(msg.text)}
        await msg.reply("💰 Сумма?")

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "take_sum")
    async def take_sum(msg: types.Message):
        if not msg.text.isdigit():
            return
        uid = admin_state[msg.from_user.id]["target"]
        add_balance(uid, -int(msg.text))
        admin_state[msg.from_user.id] = {}
        await msg.reply("✅ Успешно", reply_markup=main_kb())

    @dp.callback_query(lambda c: c.data == "adm_bal")
    async def adm_bal(call: types.CallbackQuery):
        admin_state[call.from_user.id] = {"step": "bal_id"}
        await call.message.edit_text("🆔 Айди?", reply_markup=back_kb())

    @dp.message(lambda m: admin_state.get(m.from_user.id, {}).get("step") == "bal_id")
    async def bal_id(msg: types.Message):
        if not msg.text.isdigit():
            return
        uid = int(msg.text)
        bal = get_balance(uid)
        admin_state[msg.from_user.id] = {}
        await msg.reply(
            f"👤 {uid}\\n💰 {bal} {CURRENCY}",
            reply_markup=main_kb()
        )
