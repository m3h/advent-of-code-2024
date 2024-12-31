#include <stdio.h>
#include <stdlib.h>


uint64_t combo(uint64_t operand, uint64_t registers[]) {
    if (operand <= 3) {
        return operand;
    } else if (operand == 4) {
        return registers[0];
    } else if (operand == 5) {
        return registers[1];
    } else if (operand == 6) {
        return registers[2];
    } else {
        exit(-1);
    }
}

uint64_t run(uint64_t a_init, uint64_t machine_code[], uint64_t machine_code_n)
{
    uint64_t registers[] = {a_init, 0, 0};

    uint64_t IP = 0;
    uint64_t output_len = 0;
    while (IP < machine_code_n-1) {
        const uint64_t opcode = machine_code[IP];
        const uint64_t operand = machine_code[IP+1];

        IP += 2;

        switch (opcode) {
            case 0: {
                uint64_t v = combo(operand, registers);
                if (v) {
                    registers[0] = registers[0] / (2 << (v-1));
                }
            };
            break;
            case 1: {
                registers[1] ^= operand;
            }
            break;
            case 2: {
                registers[1] = combo(operand, registers) & 0b111;
            }
            break;
            case 3: {
                if (registers[0]) {
                    IP = operand;
                }
            }
            break;
            case 4: {
                registers[1] ^= registers[2];
            }
            break;
            case 5: {
                uint64_t output = combo(operand, registers) & 0b111;
                if (output != machine_code[output_len]) {
                    return 0;
                }
                output_len += 1;
                if (output_len == machine_code_n) {
                    return 1;
                }
            }
            break;
            case 6: {
                uint64_t v = combo(operand, registers);
                if (v) {
                    registers[1] = registers[0] / (2 << (v-1));
                }
            }
            break;
            case 7: {
                uint64_t v = combo(operand, registers);
                if (v) {
                    registers[2] = registers[0] / (2 << (v-1));
                }
            }
            break;
            default: {
                printf("Unrecognized opcode: %d\n", opcode);
                exit(-2);
            }
                break;
        }

    }
    return 0;
}

int main()
{
    // insert here
    uint64_t machine_code[] = { insert here };

    for (uint64_t i = 0;; ++i) {
        if (i % 10000000 == 0) {
            printf("%llu\n", i);
        }
        if (run(i, machine_code, sizeof(machine_code) / sizeof(uint64_t))) {
            printf("Found %llu\n", i);
            return 0;
        }
    }
}