import argparse
import io
import logging
import string
import sys
from pathlib import Path
from pprint import pprint

from hilbertpiet.numbers import PushNumber
from hilbertpiet.ops import OutChar
from hilbertpiet.path import NotEnoughSpace, generate_path, map_path_u_turns, map_program_to_path
from hilbertpiet.run import Program

LOGGER = logging.getLogger(__name__)


def main():
    description = 'Generate a Hilbert-curve-shaped Piet program printing a given string'
    parser = argparse.ArgumentParser(description=description)
    input_parser = parser.add_mutually_exclusive_group()
    input_parser.add_argument('--file', '-f', type=argparse.FileType('r'),
                              dest='input', help='input string file (default stdin)')
    input_parser.add_argument('--input', '-i', type=io.StringIO,
                              dest='input', help='input string (default stdin)')
    parser.add_argument('--verbose', '-v', action='store_true', help='debug_mode')
    parser.set_defaults(input=sys.stdin)
    args = parser.parse_args()

    # Setup logging

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(levelname)s:%(name)s: %(message)s')

    # Read input

    input = ''.join(args.input.readlines())
    LOGGER.info(f'Input length = {len(input)}')

    num_chars = [ord(c) for c in input if c in set(string.printable)]
    LOGGER.info(f'Skipping {len(input) - len(num_chars)} non-ascii characters')

    LOGGER.info('')

    # Create program

    MODULE_ROOT: Path = Path(__file__).parent.parent
    PushNumber.load_numbers(MODULE_ROOT / 'data' / 'numbers.pkl')

    ops = []
    for num_char in num_chars:
        ops += [PushNumber(num_char), OutChar()]
    program = Program(ops)

    LOGGER.info(f'{program.size} codels before mapping')
    LOGGER.info('')

    # Create path and map program

    # Fine-tune necessary number of Hilbert curve iterations within a certain range
    max_iterations = 6
    iterations = 1
    success = False
    while not success:
        path = generate_path(iterations)
        path = map_path_u_turns(path)
        try:
            program = map_program_to_path(program, path)
        except NotEnoughSpace:
            if iterations >= max_iterations:
                raise
            else:
                iterations += 1
        else:
            success = True

    LOGGER.info(f'{iterations} Hilbert curve iterations')
    LOGGER.info(f'{program.size} codels after mapping')
    LOGGER.info('')

    # Run program

    context = program.run()

    # Print program output

    printable_output = context.output.strip()
    if '\n' in printable_output:
        # Indent output lines
        printable_output = '\n   ' + printable_output.replace('\n', '\n   ')
    LOGGER.debug('')

    LOGGER.info(f'Ouput: {printable_output}')
    LOGGER.info('')


if __name__ == '__main__':
    main()
