import subprocess
import time
import timeit

x = 1  #int(input("which script number?"))

var_scripts = {
    "1": "./discord_bot/2024/dis_bot.py",
    "2": "trying.py",
}

print(f"About to run {var_scripts[f'{x}']}")

start_time = time.time()
y = subprocess.run(["python3", str(var_scripts[f"{x}"])])
end_time = time.time()

execution_time = round((end_time - start_time), 2)

program_time = timeit.timeit('y', globals=globals(), number=1)
print(
    f"Successfuly ran {var_scripts[f'{x}']}\nProgram time: "
    f"{round((program_time * (10 ** 6)), 2)} μs\nExecution time: {execution_time} s"
)
