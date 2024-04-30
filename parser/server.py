import grpc
from concurrent import futures
import internship_pb2
import internship_pb2_grpc
from parser import parse_tinkoff_internships


class InternshipServicer(internship_pb2_grpc.InternshipServiceServicer):
    def GetInternships(self, request, context):
        internships_data = parse_tinkoff_internships()
        if internships_data:
            response = internship_pb2.GetInternshipsResponse()
            for category in internships_data['internships']:
                category_proto = internship_pb2.InternshipCategory(category=category['category'])
                for position in category['positions']:
                    position_proto = internship_pb2.Internship(
                        title=position['title'],
                        description=position['description'],
                        status=position['status'],
                        link=position['link'],
                        area=position['area']
                    )
                    category_proto.positions.append(position_proto)
                response.categories.append(category_proto)
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Data not found')
            return internship_pb2.GetInternshipsResponse()


def serve():
    print("Starting server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    internship_pb2_grpc.add_InternshipServiceServicer_to_server(InternshipServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped manually.")
        server.stop(0)


if __name__ == '__main__':
    serve()
