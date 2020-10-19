#!/usr/bin/env python3

import asyncio
import os

from yapapi.log import enable_default_logger, log_summary, log_event_repr # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta


async def main(subnet_tag = "testnet"):
    with open(".image.hash") as f:
        hash = f.read()
    package = await vm.repo(
        image_hash = hash,
        min_mem_gib = 0.5,
        min_storage_gib = 2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        if len(tasks) < 2:
            raise "Need at least 2 tasks!"
        async for i, task in enumerate(tasks):
            frames = ['0', '1', '2'] if i == 0 else ['3', '4', '5']
            framesStr = ' '.join(frames)
            ctx.run("/bin/bash", "-c", f"cd /root && ./plot.py {framesStr} > log.txt 2>&1")
            for frame in frames:
                ctx.download_file(f"/root/frame{frame}.png", f"frame{frame}.png")
            # ctx.download_file(f"/root/log.txt", f"log.txt")
            yield ctx.commit()
            task.accept_task()

        ctx.log(f"frames created.")

    jobs: range = range(0, 1, 1)
    init_overhead: timedelta = timedelta(minutes = 1)
    async with Engine(
        package = package,
        max_workers = 2,
        budget = 1000,
        timeout = init_overhead + timedelta(minutes = 1),
        subnet_tag = subnet_tag,
        event_emitter = log_summary(log_event_repr),
    ) as engine:

        async for job in engine.map(worker, [Task(data = job) for job in jobs]):
            print(f"[job done: {job}, result: {job.output}")
    
    if os.system("convert -delay 200 -loop 0 frame*.png plot.gif"):
        raise "Cannot execute `convert`."


enable_default_logger()
loop = asyncio.get_event_loop()
job = loop.create_task(main(subnet_tag = "devnet-alpha.2"))
try:
    asyncio.get_event_loop().run_until_complete(job)
except (Exception, KeyboardInterrupt) as e:
    print(e)
    job.cancel()
    asyncio.get_event_loop().run_until_complete(job)
