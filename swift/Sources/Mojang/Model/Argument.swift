//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

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
