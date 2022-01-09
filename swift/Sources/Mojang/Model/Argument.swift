//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct Argument: MojangCodable {
    public let game: [GameOption]
    public let jvm: [JVMOption]
    
    public enum GameOption: MojangCodable {
        case object(GameOptionObj)
        case string(String)
        
        public init(from decoder: Decoder) throws {
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
        
        public func encode(to encoder: Encoder) throws {
            var container = encoder.singleValueContainer()
            switch self {
            case .string(let value):
                try container.encode(value)
            case .object(let obj):
                try container.encode(obj)
            }
        }
    }
    
    public struct GameOptionObj: MojangCodable {
        let rules: [Rule]
        let value: OptionValue
        
        struct Rule: MojangCodable {
            let action: String
            let features: Feature
            
            struct Feature: MojangCodable {
                let isDemoUser: Bool?
                let hasCustomResolution: Bool?
            }
        }
    }
    
    public enum JVMOption: MojangCodable {
        case object(JVMOptionObj)
        case string(String)
        
        public init(from decoder: Decoder) throws {
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
        
        public func encode(to encoder: Encoder) throws {
            var container = encoder.singleValueContainer()

            switch self {
            case .string(let value):
                try container.encode(value)
            case .object(let obj):
                try container.encode(obj)
            }
        }
    }
    
    public struct JVMOptionObj: MojangCodable {
        public let rules: [Rule]
        public let value: OptionValue
        
        public struct Rule: MojangCodable {
            public let action: String
            public let os: OS
            public struct OS: MojangCodable {
                public let name: String?
                public let arch: String?
                public let version: String?
            }
        }
    }
    
    public enum OptionValue: MojangCodable {
        case array([String])
        case string(String)
        
        public init(from decoder: Decoder) throws {
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
        
        public func encode(to encoder: Encoder) throws {
            
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
