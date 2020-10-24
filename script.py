#!/usr/bin/env python3
# Adapted from Golem tutorial code by Jude Hungerford
import os
import asyncio
import utils
import sys
import subprocess
import time
import numpy as np
from datetime import timedelta
from yapapi.log import enable_default_logger, log_summary, log_event_repr
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext

def renderAnimation(ctx=None, tasks=None):
    if os.system("convert -delay 200 -loop 0 frame*.png plot.gif"):
        raise "Cannot execute `convert`."

GOLEM_WORKDIR = '/golem/work/'

async def main(args):

    with open(".image.hash") as f:
        hash = f.read()
    package = await vm.repo(
        image_hash=hash,
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        tasks_count = 0
        async for task in tasks:
            frames = [['0', '1', '2'], ['3', '4', '5']][task.data]
            framesStr = ' '.join(frames)
            ctx.run("/bin/bash", "-c", f"cd {GOLEM_WORKDIR} && /root/plot.py {framesStr} > {GOLEM_WORKDIR}log.txt 2>&1")
            for frame in frames:
                ctx.download_file(f"{GOLEM_WORKDIR}log.txt", f"log{task.data}.txt")
                ctx.download_file(f"{GOLEM_WORKDIR}frame{frame}.png", f"frame{frame}.png")
            yield ctx.commit()
            task.accept_task()
            tasks_count += 1
        # if tasks_count < 2:
        #     raise "Need at least 2 tasks!"

    async with Engine(
        package=package,
        max_workers=args.number_of_providers,
        budget=10.0,
        # timeout should be keyspace / number of providers dependent
        timeout=timedelta(minutes=25),
        subnet_tag=args.subnet_tag,
        event_emitter=log_summary(log_event_repr),
    ) as engine:

        inputs = range(2)

        async for task in engine.map(worker, [Task(data=graphInput) for graphInput in inputs]):
            print(
                f"{utils.TEXT_COLOR_CYAN}"
                f"Task computed: {task}, result: {task.output}"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )


if __name__ == "__main__":
    parser = utils.build_parser("script")
    parser.add_argument("--number-of-providers", dest="number_of_providers", type=int, default=2)
    args = parser.parse_args()
    enable_default_logger(log_file=args.log_file)
    sys.stderr.write(
        f"Using subnet: {utils.TEXT_COLOR_YELLOW}{args.subnet_tag}{utils.TEXT_COLOR_DEFAULT}\n"
    )

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args))

    try:
        # Generate a new set of images on the Golem network
        loop.run_until_complete(task)
        # Combine them locally
        renderAnimation()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        loop.run_until_complete(task)

