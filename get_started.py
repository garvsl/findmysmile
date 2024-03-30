import modal

stub = modal.Stub("example-get-started")

@stub.functions()
def square(x):
    print("This code is running on a remote worker!")
    return x ** 2

@stub.local_entrypoint()
def main: 
    print("The square is", square.remote(42))