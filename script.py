import asyncio

from yapapi.log import enable_default_logger, log_summary, log_event_repr # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta


async def main(subnet_tag = "testnet"):
    package = await vm.repo(
        image_hash = "limit-visualization",
        min_mem_gib = 0.5,
        min_storage_gib = 2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            ctx.run("/bin/bash", "-c", "cd /root && ./plot.py > log.txt 2>&1")
            output_file = f"plot.gif"
            ctx.download_file(f"/root/plot.gif", output_file)
            ctx.download_file(f"/root/log.txt", f"log.txt")
            yield ctx.commit()
            task.accept_task(result=output_file)

        ctx.log(f"image created.")

    jobs: range = range(0, 1, 1)
    init_overhead: timedelta = timedelta(minutes = 1)
    async with Engine(
        package = package,
        max_workers = 1,
        budget = 1000,
        timeout = init_overhead + timedelta(minutes = 1),
        subnet_tag = subnet_tag,
        event_emitter = log_summary(log_event_repr),
    ) as engine:

        async for job in engine.map(worker, [Task(data = job) for job in jobs]):
            print(f"[job done: {job}, result: {job.output}")


enable_default_logger()
loop = asyncio.get_event_loop()
job = loop.create_task(main(subnet_tag = "devnet-alpha.2"))
try:
    asyncio.get_event_loop().run_until_complete(job)
except (Exception, KeyboardInterrupt) as e:
    print(e)
    job.cancel()
    asyncio.get_event_loop().run_until_complete(job)
