from aiogram.fsm.context import FSMContext
from analysis import reports
from database import server_db, object_storage
from app.fsm import Consultant
from assets import text_samples
from aiogram import types, F, Router
from dotenv import load_dotenv
from aiogram.types import Message, BufferedInputFile


load_dotenv()
consultant_router = Router()


@consultant_router.message(F.text == text_samples.get_report_for_client)
async def get_client_id(message: Message, state: FSMContext):
    await message.answer(text_samples.type_client_id)
    await state.set_state(Consultant.client_id)


@consultant_router.message(Consultant.client_id)
async def prepare_report(message: Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        account_id = int(message.text)
        report_item = await server_db.create_report(int(session_id))
        await reports.create_account_financial_consulting_report(account_id, report_item['report_id'])
        pdf_report = await object_storage.get_report(report_item['report_id'])
        await message.answer_document(document=BufferedInputFile(file=pdf_report,
                                                                 filename=f'Финансовая консультация {report_item["report_id"]}.pdf'))
        await state.clear()
    except Exception as e:
        await message.answer(text_samples.client_not_found + '\nПопробуйте еще раз, нажав на кнопку.' + '\n\n' + str(e))
    await state.clear()