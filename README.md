# ichi_simulator

ichi 指令集的模拟器

ichi 为个人出于学习目的设计的一种指令集，即日语中「一」的罗马音 

------------------------------------

## 基本参数

字长为 16 位，内存地址范围 0x0000 - 0xFFFF 
程序可用范围  0x0000 - 0x5FFF 其余为保留地址
上电时 PC 被初始化为 0x0200
小段序，按字节寻址

## 寄存器

处于容易实现的目的，暂时共有 6 个寄存器,均为 16 位，功能如下所示：

| 寄存器名称 | 作用           | 代号（十六进制） |
| ----- | ------------ | -------- |
| AX    |              | 00       |
| BX    |              | 01       |
| CX    |              | 02       |
| DX    |              | 03       |
| PC    | 程序计数器        | 10       |
| SP    | 栈顶寄存器        | 11       |
| BP    | 栈基址寄存器       | 12       |
| FLAG  | 储存运算过程中产生的标志 | 13       |

## 机器指令

为了方便实现，所有指令长度均为两个字长，即 32 位

### 存取相关
| 指令名称                | 指令作用                         | 指令格式（十六进制）             |
| ------------------- | ---------------------------- | ---------------------- |
| LOADN [立即数]         | 将某个数存储到 AX 寄存器               | 0000 [立即数]             |
| LOADP               | 读取 DX 寄存器中指向的内存，存储到 AX 寄存器   | 0001 0000              |
| STOREP              | 保存 AX 寄存器中的内容到 DX 寄存器指向的内存地址 | 0002 0000              |
| MOV  [目标寄存器] [原寄存器] | 移动某个寄存器的内容到另外一个寄存器           | 0003 [目标寄存器编号][原寄存器编号] |

### 运算相关


| 指令名称   | 指令作用                                | 指令格式（十六进制） |
| ------ | ----------------------------------- | ---------- |
| ADD    | 将 AX 与 BX 的内容相加，结果保存到 AX            | 0010 0000  |
| OR     | 将 AX 与 BX 的内容做按位或运算，结果保存到 AX        | 0011 0000  |
| AND    | 将 AX 与 BX 的内容做按位和运算，结果保存到 AX        | 0012 0000  |
| NOT    | 将 AX 的内容做按位非运算，结果保存到 AX             | 0013 0000  |
| XOR    | 将 AX 与 BX 的内容做异或运算，结果保存到 AX         | 0014 0000  |
| LSHIFT | 将 AX 的内容左移 BX 位，结果保存到 AX            | 0015 0000  |
| RSHIFT | 将 AX 的内容右移 BX 位，结果保存到 AX            | 0016 0000  |
| LE     | 比较 AX 和 BX 的内容，若小于则将 FLAG 置 1，否则置 0 | 0017 0000  |
| GT     | 比较 AX 和 BX 的内容，若大于则将 FLAG 置 1，否则置 0 | 0018 0000  |
| EQ     | 比较 AX 和 BX 的内容，若等于则将 FLAG 置 1，否则置 0 | 0019 0000  |

### 流程控制相关


| 指令名称 | 指令作用                          | 指令格式（十六进制） |
| ---- | ----------------------------- | ---------- |
| JMP  | 当FLAG不为0时，将 DX 赋值给 PC 寄存器（跳转） | 0020 0000  |
| NOP  | 空指令，填充使用                      | 0021 0000  |
| HALT | 停机                            | 0022 0000  |


遇到非法指令时，会产生一个软中断，将下一条指令的地址写入 DX,并将 PC 置于 0x0100 处执行
