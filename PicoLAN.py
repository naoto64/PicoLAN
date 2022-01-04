class PicoLAN:
    from machine import UART, Pin
    
    __STX = b"\x02"
    __ETX = b"\x03"
    
    __WAIT_STX = 0
    __WAIT_ADDR = 1
    __WAIT_SIZE = 2
    __WAIT_ETX = 3
    __ARGUMENT_DATA_MAX = 9999
    
    DATA_LEN_FIXED = 0
    DATA_LEN_VARIABLE = 1

    __read_state = __WAIT_STX
    __read_buff = b""
    __read_count = 0
    __dict_handler = None
    
    def __init__(self, _id, baudrate, tx, rx, addr, handler, addr_max=256, data_max=256, data_len_mode=self.DATA_LEN_FIXED):
        if not isinstance(addr, int):
            raise ValueError("\"addr\" is not an int type.")

        if not isinstance(addr_max, int):
            raise ValueError("\"addr_max\" is not an int type.")

        if not isinstance(data_max, int):
            raise ValueError("\"data_max\" is not an int type.")
        elif :
            raise ValueError("The range of values for data_max is 0 to {}.".format(self.__ARGUMENT_DATA_MAX))
        else:
            self.__DATA_MAX = data_max

        if addr > addr_max or addr < 0:
            raise ValueError("The value of \"addr\" is out of range.")
        else:
            self.__ADDR = str(addr).encode("UTF-8")

        if callable(handler):
            self.__handler = handler:
        else:
            raise ValueError("\"handler\" is not a function.")

        if addr_max < 0:
            raise ValueError("The value of \"addr_max\" is negative.")
        elif addr_max < 10:
            self.__ADDR_LEN = 1
        elif addr_max < 100:
            self.__ADDR_LEN = 2
        elif addr_max < 1000:
            self.__ADDR_LEN = 3
        else:
            raise ValueError("The value of addr_max is too large.")

        if data_max < 0:
            raise ValueError("The value of \"data_max\" is negative.")
        elif data_max < 10:
            self.__DATA_LEN = 1
        elif data_max < 100:
            self.__DATA_LEN = 2
        elif data_max < 1000:
            self.__DATA_LEN = 3
        elif data_max < 10000:
            self.__DATA_LEN = 4
        else:
            raise ValueError("The value of data_max is too large.")

        if data_len_mode != self.DATA_LEN_FIXED and data_len_mode != self.DATA_LEN_VARIABLE:
            raise ValueError("The value of data_len_mode is invalid.")
        else:
            self.__DATA_LEN_MODE = data_len_mode

        self.__READ_MAX = self.__ADDR_LEN + self.__DATA_LEN + 2
        self.uart = UART(_id, baudrate, tx, rx)
        
    def read(self):
        if self.uart.any() >= 1:
            read_data = self.uart.read(1)
            self.__read_count += 1
            print(read_data)
            if self.__read_state == self.__WAIT_STX:
                if read_data == self.__STX:
                    self.__read_state = self.__WAIT_ADDR
                else:
                    __read_reset()
            elif self.__read_state == self.__WAIT_ADDR:
                if self.__read_count < self.__ADDR_LEN + 1:
                    pass
                elif self.__read_count == self.__ADDR_LEN + 1 and read_data == self.__ADDR[self.__ADDR_LEN]:
                    self.__read_state = self.__WAIT_SIZE
                elif self.__read_count < self.__ADDR_LEN + 1:
                    __read_reset()
            elif self.__read_state == self.__WAIT_SIZE:
                if self.__read_count < self.__ADDR_LEN + self.__DATA_LEN + 1:
                    pass
                else:
                    self.__read_state = self.__WAIT_ETX
            elif self.__read_state == self.__WAIT_ETX:
                if read_data == self.__ETX:
                    if self.__read_count == self.__READ_MAX:
                        self.__data_read(self.__read_buff.decode("UTF-8"))
                    __read_reset()
                elif self.__read_count >= self.__READ_MAX:
                    __read_reset()
                elif read_data < b"\x20" or read_data > b"\x7E":
                    __read_reset()
                else:
                    self.__read_buff += read_data
    
    def send(self, data, addr, sep=" ", arg_sep="="):
        send_data = sep
        for key in data:
            send_data += key
            if data[key] is not None:
                send_data += arg_sep + data
            send_data += sep
        send_data = send_data[1:]
        if len(send_data) <= self.__DATA_MAX:
            format_str = "{: <" + str(self.__DATA_LEN) + "}"
            send_data = self.__STX + self.__ADDR + format_str.format(send_data).encode("UTF-8") + self.__ETX
            self.uart.write(send_data)

    def __read_reset(self):
        self.__read_buff = b""
        self.__read_state = self.__WAIT_STX
        self.__read_count = 0
        
    def __data_read(self, read_data, sep=" ", arg_sep="="):
        data_list = read_data.split(sep)
        data_dict = {}
        if len(data_list) >= 2:
            for data in data_list:
                arg = data.split(arg_sep)
                if len(arg) != 2:
                    data_dict[data_list] = None
                else:
                    data_dict[arg[0]] = arg[1]
        else:
            data_dict[read_data] = None
        self.__handler(data_dict)
