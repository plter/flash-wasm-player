import asyncio
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RUFFLE_DIR = os.path.join(CURRENT_DIR, "ruffle")
RUFFLE_WEB_DIR = os.path.join(RUFFLE_DIR, "web")


async def shell(*args):
    print(args)
    p = await asyncio.create_subprocess_shell(*args)
    code = await p.wait()
    if code:
        print(f"exit with none zero code: {code}")
    return code


async def main():
    if "-l" in sys.argv:
        if await shell(f"cp -rf {os.path.join(CURRENT_DIR,'replacements')}/* {RUFFLE_DIR}"):
            return
        if await shell(f"cd {RUFFLE_WEB_DIR} && npm run build"):
            return
    else:
        print("If you want to build local source only, please use 'python build.py -l'")
        if os.path.exists(RUFFLE_DIR):
            code = await shell(f"cd {RUFFLE_DIR} && git pull")
        else:
            code = await shell("git clone git@github.com:ruffle-rs/ruffle.git")
        if code:
            return
        if await shell(f"cp -rf {os.path.join(CURRENT_DIR,'replacements')}/* {RUFFLE_DIR}"):
            return
        if await shell(f"cd {RUFFLE_WEB_DIR} && npm run bootstrap && npm run build"):
            return
    if await shell(f"cp -rf {os.path.join(RUFFLE_WEB_DIR,'packages','selfhosted','dist')} {CURRENT_DIR}"):
        return

if __name__ == "__main__":
    asyncio.run(main())
