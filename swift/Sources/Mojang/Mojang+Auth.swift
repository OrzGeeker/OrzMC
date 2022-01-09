//
//  File.swift
//  
//
//  Created by joker on 2022/1/9.
//

import Foundation

public extension Mojang {
    enum AuthAPI {
        private static let baseUrl = "https://authserver.mojang.com"
        private static let encoder = JSONEncoder()
        
        case authenticate(reqParam: AuthReqParam)
        case validate(reqParam: ValidateReqParam)
        case refresh(reqParam: ValidateReqParam)
        
        public var data: Data? {
            get async throws {
                guard let reqURL = URL(string: AuthAPI.baseUrl)
                else {
                    return nil
                }
                
                var endpoint: String? = nil
                var bodyData: Data? = nil
                
                switch self {
                case .authenticate(let reqParam):
                    endpoint = "authenticate"
                    bodyData = try AuthAPI.encoder.encode(reqParam)
                case .validate(let reqParam):
                    endpoint = "validate"
                    bodyData = try AuthAPI.encoder.encode(reqParam)
                case .refresh(let reqParam):
                    endpoint = "refresh"
                    bodyData = try AuthAPI.encoder.encode(reqParam)
                }
                
                guard let path = endpoint
                else{
                    return nil
                }
                let URL = reqURL.appendingPathComponent(path)
                var request = URLRequest(url: URL)
                request.httpMethod = "POST"
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
                request.httpBody = bodyData
                
                let (data, response) = try await URLSession.shared.data(for: request)
                guard (response as? HTTPURLResponse)?.statusCode == 200
                else {
                    let error = try JSONDecoder().decode(AuthRespError.self, from: data)
                    print(error)
                    return nil
                }
                return data
            }
        }
        
        public struct AuthReqParam: Encodable {
            public let agent: Agent
            public let username: String
            public let password: String
            public let clientToken: String?
            
            public init(agent: Agent = Agent(), username: String, password: String, clientToken: String? = nil) {
                self.agent = agent
                self.username = username
                self.password = password
                self.clientToken = clientToken
            }
            
            public struct Agent: Encodable {
                public let name: String
                public let version: Int
                
                public init(name: String = "Minecraft", version: Int = 1) {
                    self.name = name
                    self.version = version
                }
            }
        }
        
        public struct AuthRespone: Decodable {
            public let accessToken: String
            public let clientToken: String
            public let availableProfiles: [AvailableProfile]
            public let selectedProfile: AvailableProfile?
            
            public struct AvailableProfile: Decodable {
                public let id: String
                public let name: String
            }
        }
        
        public struct AuthRespError: Decodable {
            public let error: String
            public let errorMessage: String
            public let cause: String?
        }
        
        public struct ValidateReqParam: Encodable {
            public let accessToken: String
            public let clientToken: String?
        }
    }
}
