import sys
from simulator_fake import TinyBASUSimulator as Simulator

# Entry point: parses CLI args, builds the simulator, runs it, and writes the final report.
def main():

    
    if len(sys.argv) != 6:
        print("Usage: python sim.py [total_cycles] [prediction_method] [inst_file] [data_file] [report_file]")
        return

    
    timeout_cycles = int(sys.argv[1])
    prediction_method = sys.argv[2]
    inst_file = sys.argv[3]
    data_file = sys.argv[4]
    report_file = sys.argv[5]

    simulator = Simulator(prediction_method)
    simulator.parse_instruction(inst_file)
    simulator.init_memory(data_file)
    simulator.run(timeout_cycles)
    simulator.report(report_file)


if __name__ == '__main__':
    main()
