//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/7.
//

import Foundation

public struct Mojang {
    
    static let jsonDecoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder;
    }()
    
    static let jsonEncoder: JSONEncoder = {
       let encoder = JSONEncoder()
        encoder.outputFormatting = [
            .prettyPrinted,
            .sortedKeys,
            .withoutEscapingSlashes
        ]
        encoder.keyEncodingStrategy = .convertToSnakeCase
        return encoder
    }()
    
    /// 获取版本信息
    static var manifest: Manifest? {
        get async throws {
            let url = URL(string: "https://launchermeta.mojang.com/mc/game/version_manifest.json")!
            let (data, response) = try await URLSession.shared.data(from: url)
            guard (response as? HTTPURLResponse)?.statusCode == 200
            else {
                return nil
            }
            return try Mojang.jsonDecoder.decode(Manifest.self, from: data)
        }
    }
    
    /// Manifest Model
    public struct Manifest: Codable {
        
        let latest: Latest
        let versions: [Version]
        
        struct Latest: Codable {
            let release: String
            let snapshot: String
        }
        
        struct Version: Codable {
            let id: String
            let type: String
            let url: URL?
            let time: String
            let releaseTime: String
            
            var gameInfo: GameInfo? {
                get async throws {
                    guard let url = self.url
                    else {
                        return nil
                    }
                    let (data, response) = try await URLSession.shared.data(from: url)
                    guard (response as? HTTPURLResponse)?.statusCode == 200
                    else {
                        return nil
                    }
                    return try Mojang.jsonDecoder.decode(GameInfo.self, from: data)
                }
            }
            
            struct GameInfo: Codable {
                let arguments: Argument
                let assetIndex: AssetIndex
                let assets: String
                let complianceLevel: Int
                let downloads: Download
                let id: String
                let javaVersion: JavaVersion
                let libraries: [JavaLibrary]
                let logging: Logging
                let mainClass: String
                let minimumLauncherVersion: Int
                let releaseTime: String
                let time: String
                let type: String
                
                struct Argument: Codable {
                    let game: [GameOption]
                    let jvm: [JVMOption]
                    
                    enum GameOption: Codable {
                        case object(GameOptionObj)
                        case string(String)
                        
                        init(from decoder: Decoder) throws {
                            let container = try decoder.singleValueContainer()
                            
                            if let string = try? container.decode(String.self) {
                                self = .string(string)
                            }
                            else if let obj = try? container.decode(GameOptionObj.self) {
                                self = .object(obj)
                            }
                            else {
                                throw DecodingError.typeMismatch(GameOptionObj.self, .init(codingPath: decoder.codingPath, debugDescription: "Wrong type for GameOptionObj"))
                            }
                        }
                        
                        func encode(to encoder: Encoder) throws {
                            var container = encoder.singleValueContainer()
                            switch self {
                            case .string(let value):
                                try container.encode(value)
                            case .object(let obj):
                                try container.encode(obj)
                            }
                        }
                    }
                    
                    struct GameOptionObj: Codable {
                        let rules: [Rule]
                        let value: OptionValue
                        
                        struct Rule: Codable {
                            let action: String
                            let features: Feature
                            
                            struct Feature: Codable {
                                let isDemoUser: Bool?
                                let hasCustomResolution: Bool?
                            }
                        }
                    }
                    
                    enum JVMOption: Codable {
                        case object(JVMOptionObj)
                        case string(String)
                        
                        init(from decoder: Decoder) throws {
                            let container = try decoder.singleValueContainer()
                            if let string = try? container.decode(String.self) {
                                self = .string(string)
                            }
                            else if let jvmOptObj = try? container.decode(JVMOptionObj.self) {
                                self = .object(jvmOptObj)
                            }
                            else {
                                throw DecodingError.typeMismatch(JVMOptionObj.self, .init(codingPath: decoder.codingPath, debugDescription: "Wrong type for JVMOptionObj"))
                            }
                        }
                        
                        func encode(to encoder: Encoder) throws {
                            var container = encoder.singleValueContainer()

                            switch self {
                            case .string(let value):
                                try container.encode(value)
                            case .object(let obj):
                                try container.encode(obj)
                            }
                        }
                    }
                    
                    struct JVMOptionObj: Codable {
                        let rules: [Rule]
                        let value: OptionValue
                        
                        struct Rule: Codable {
                            let action: String
                            let os: OS
                            struct OS: Codable {
                                let name: String?
                                let arch: String?
                                let version: String?
                            }
                        }
                    }
                    
                    enum OptionValue: Codable {
                        case array([String])
                        case string(String)
                        
                        init(from decoder: Decoder) throws {
                            let container = try decoder.singleValueContainer()
                            
                            if let string = try? container.decode(String.self) {
                                self = .string(string)
                            }
                            else if let array = try? container.decode([String].self) {
                                self = .array(array)
                            }
                            else {
                                throw DecodingError.typeMismatch([String].self, .init(codingPath: decoder.codingPath, debugDescription: "Wrong type for [String]"))
                            }
                        }
                        
                        func encode(to encoder: Encoder) throws {
                            
                            var container = encoder.singleValueContainer()
                            
                            switch self {
                            case .string(let value):
                                try container.encode(value)
                            case .array(let array):
                                try container.encode(array)
                            }
                        }
                    }
                }
                
                struct AssetIndex: Codable {
                    let id: String
                    let sha1: String
                    let size: Int64
                    let totalSize: Int64
                    let url: URL
                }
                
                struct Download: Codable {
                    let client: Asset
                    let clientMappings: Asset
                    let server: Asset
                    let serverMappings: Asset
                    
                    struct Asset: Codable {
                        let sha1: String
                        let size: Int64
                        let url: URL
                    }
                }
                
                struct JavaVersion: Codable {
                    let component: String
                    let majorVersion: Int
                }
                
                struct JavaLibrary: Codable {
                    let downloads: Download
                    let name: String
                    
                    struct Download: Codable {
                        let artifact: Artifact
                        
                        struct Artifact: Codable {
                            let path: String
                            let sha1: String
                            let size: Int64
                            let url: URL
                        }
                    }
                }
                
                struct Logging: Codable {
                    let client: Client
                    
                    struct Client: Codable {
                        let argument: String
                        let file: File
                        let type: String
                        
                        struct File: Codable {
                            let id: String
                            let sha1: String
                            let size: Int64
                            let url: URL
                        }
                    }
                }
            }
        }
    }
}
