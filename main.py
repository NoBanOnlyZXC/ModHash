import platform
from datetime import datetime
startTime = datetime.now()
from pathlib import Path
import os, sys
from pyrogram import Client, idle
from utils import misc, cfgmaster
from utils.scripts import start
from utils.loader import import_module

start.init()

from utils import log

script_path = os.path.dirname(os.path.realpath(__file__))
if script_path != os.getcwd():
    os.chdir(script_path)
if not 'restart' in sys.argv:
    misc.user.account = start.user()
else:
    misc.user.account = sys.argv[2]

app = Client(
    name = misc.user.account,
    api_id = misc.api_id,
    api_hash = misc.api_hash,
    app_version = misc.userbot_version,
    device_model = misc.userbot_name,
    system_version = platform.version() + " " + platform.machine(),
    workdir = misc.session_path
)

os.system('cls')

async def main():
    await cfgmaster.start(app)
    await app.start()
    log.write.info("Main","Userbot starting")

    misc.user.me = await app.get_me()
    me = misc.user.me
    log.write.info('Main',f'Starting on account: {me.first_name} {me.id} / {me.phone_number}')

    success_modules = 0
    failed_modules = 0

    success_modules_list = []
    failed_modules_list = []

    for path in Path('modules').rglob('*.py'):
        try:
            import_module(path.stem, app)
        except Exception as e:
            failed_modules += 1
            failed_modules_list.append(path.stem)
            #raise # For debugging modules error
        else:
            log.write.info('imports.main',f'import {path.stem} success.')
            success_modules = success_modules + 1
            success_modules_list.append(path.stem)
    os.system('cls')
    if success_modules:
        print(f'Загружено {success_modules} модулей.\nСписок: {" ".join(success_modules_list)}')
        log.write.info("Main", f'Loaded {success_modules} modules.\n\tList: {" ".join(success_modules_list)}')
    if failed_modules:
        print(f'Не удалось загрузить {failed_modules} модулей.\nСписок: {" ".join(failed_modules_list)}')
        log.write.warn("Main", f'Not loaded {failed_modules} modules.\n\tList: {" ".join(failed_modules_list)}')
    
    print(f"{misc.userbot_name} {misc.userbot_version} запущен.")
    log.write.info('Main', f"{misc.userbot_name} {misc.userbot_version} started")

    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())