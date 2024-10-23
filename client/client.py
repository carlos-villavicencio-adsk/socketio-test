import time
from socketIO_client_nexus import SocketIO
from socketIO_client_nexus.exceptions import TimeoutError


def data_callback(type):
    def callback(data=None):
        print(f"{type} event: {data}")
    return callback


def wait_for_response(socketIO, timeout=0.1, single_loop=False, process_events=True):
    process_new_messages(
            socketIO,
            wait=float(timeout),
            single_loop=single_loop,
            process_events=process_events,
        )
    

def process_new_messages(socketIO, wait=0.01, single_loop=False, process_events=True):
        try:
            socketIO._heartbeat_thread.hurry()
            socketIO._transport.set_timeout(seconds=0.1)
            start = time.time()

            while wait >= (time.time() - start) or single_loop:
                try:
                    socketIO._process_packets()
                except IndexError as e:
                    print(f"IndexError: {e}")
                except TimeoutError:
                    # print("Expected timeout")
                    ...
                else:
                    if single_loop:
                        break
        finally:
            socketIO._heartbeat_thread.relax()
            socketIO._transport.set_timeout()
    

if __name__ == "__main__":
    socketIO = SocketIO('http://localhost', 3000)

    socketIO.on("return", data_callback("return"))
    socketIO.on("disconnect", data_callback("disconnect"))
    socketIO.on("progress", data_callback("progress"))
    socketIO.on("complete", data_callback("complete"))
    socketIO.on("server_response", data_callback("server_response"))

    socketIO.emit("execute_command", {'message': 'Please give me data!'})
    while True:
        wait_for_response(socketIO, single_loop=True, process_events=False)
