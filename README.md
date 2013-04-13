simulator-demo
==============

An Internet simulator. This demonstrates how to simulate a multi-threaded paradigm.

##Explanation##

`sim.simulator` is the singleton instance of `sim.Simulator` controls the flow of the simulation.

There are two types of functions: "instantaneous" and "non-instantaneous". Non-instantaneous
functions can only be called by other non-instantaneous function. All functions may be define as
non-instantaneous, if desired.

(1) Instantaneous - Define these functions as you would normally.
 
    def harmonic_mean(*numbers):
        return len(numbers) / sum(map(lambda x: 1/x, numbers))


(2) Non-instantaneous - Define a generator instead of a function. To make other calls to
non-instantaneous function, use `yield`. You may also use `yield` to collect the return value of
the call. Return values as normal. (As usual, no return value returns `None`.)

    def accept_one_conn(socket):
        socket1 = yield socket.accept()
        yield socket1.send('hi')
        some_bytes = yield socket.receive()
        socket1.close()
        return some_bytes

To have the current "thread" sleep, use the non-instantaneous `sim.sleep(timeout)`:
    
    from sim import simulator, sleep
    def print_times():
        for _ in xrange(10):
            print simulator.scheduler.get_time()
            yield sleep(1000)

A new thread may be spawned from any function by passing `sim.simulator.new_thread()` a
non-instantaneous function.
    
    from sim import simulator
    def accept_conns(socket):
        socket1 = socket.accept()
        simulator.new_thread(handle_conn(socket1))
    
    def handle_conn(socket):
        #blah blah
        yield socket.close()
