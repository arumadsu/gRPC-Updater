# Команда для генерации protobuf файлов для обеих папок
proto:
	python3 -m grpc_tools.protoc -I ./protobufs --python_out=./frontend --grpc_python_out=./frontend ./protobufs/updater.proto
	python3 -m grpc_tools.protoc -I ./protobufs --python_out=./backend --grpc_python_out=./backend ./protobufs/updater.proto

# Команда для быстрой очистки сгенерированных файлов (очень полезно при ошибках!)
clean:
	rm -f frontend/*_pb2*.py
	rm -f backend/*_pb2*.py