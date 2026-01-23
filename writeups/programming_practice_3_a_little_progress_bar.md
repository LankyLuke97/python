## A Little Progress (Bar)

For some reason, a small but persistent question once lodged in my head: how do programs manage an in-place progress bar? Specifically, when writing to the terminal, how does one get those little displays that look something like the below:  

```#####........```

Where each time progress occurs, the bar is overwritten. It wasn't just something as basic as progress bars - more complex examples that come to mind would be ASCII-based games like Dwarf Fortress - but the underlying curiosity is the same. How does output to the terminal actually work?  

This may well seem trivial to most experienced programmers, but I think the lack of understanding it might display speaks to how far removed we are from the actual computer and its peripherals these days; bearing in mind that I concluded my university studies prior to the rise of AI, even then I had never really played with something as basic as terminal I/O; certainly not to the extent of understanding the progress bar.  

While working my way through Fluent Python by Luciano Romalho, he gives a didactic example (when starting the discussion around multiprocessing, multithreading, and asynchronous coroutines) of a simple ASCII spinner, that cycles through the characters '\|/-' simulate a 'spinner'. The trick to making this work, of course, is that each character must be in the same spot, to trick the brain into seeing movement where there is none.  

Though this was a toy example, it had enough information to jog me into playing around with a toy progress bar, the final iteration of which is in the code block below:  

```
1 def progress_bar(steps: int, delay: float) -> None:
2    cols = shutil.get_terminal_size().columns
3    for i in range(p+1):
4        cols_filled = int((i / p) * cols)
5        print(f"\r{'#' * (cols_filled)}{'.' * (cols - cols_filled)}", end='', flush=True)
6        time.sleep(delay)
7    print(f"\r{' '*cols}",end='',flush=True)
8    print(f"\rComplete!")
```

The key is understanding what happens with characters in the terminal, which I had never really given thought to. In general usage within the terminal, the behaviour seems to allow for abitrary editing in the current line, and then seems to treat each completed line as immutable, something you can move only vertically but can't edit. What the example showed, however, was a different model of how characters work.  

The place to start is the print function in line 5. I did not realise there are options that can be provided to print. The first of these here is the *end* keyword. By default, this is the newline character, which is what makes the terminal move to a new line on printing, rather than this being some inbuilt functionality. By replacing the newline with an empty string, successive print statements will write to the same line.  

The next is the *flush* keyword. Rather than directly writing to the stdout at all times, print is storing the provided objects in a buffer. The buffer then gets written to stdout once the buffer is full, or once a newline character is encountered. Since each print statement ends with that newline character by default, the behaviour is *normally* to write the objects immediately - but *flush* is actually defaulted to **false**, meaning that the output will not show now, since I have removed the newline character. By setting *flush* to **true**, the print statement will ensure text is still written immediately to stdout.  

Next, and really finally for the basic functionality of this, the carriage return character (\r) is added to the start of each printed string. Deriving its name from the lever on a typewriter that returned the *carriage* of paper to the write, aligning the type element with the left of the paper, this character moves the output back to the left of the terminal, and further output will start there. However, it does not *clear* the previous characters - new output will overwrite the previous characters.  

In this example, then, each line is output the full width of the terminal (determined with the shutil.get_terminal_size function, which returns number of columns and lines in the current terminal screen), with an ever-increasing ratio of pound symbols to periods. At the end, a row of spaces is printed, effectively clearing the output, and a completion message is displayed.  

Whilst this is a very small toy example, without even proper error handling or any concept of a real process to represent progress, I still enjoyed getting a little better understanding of the terminal and stdout. I wonder if the next stage would be some sort of little ASCII game in Python, to experiment with colours, multiple lines, and other effects.  


