//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/26.
//

import Foundation

extension JSONDecoder.KeyDecodingStrategy {
    
    static var convertFromKebabCase: JSONDecoder.KeyDecodingStrategy = .custom { keys in
        let codingKey = keys.last!
        let key = codingKey.stringValue
        guard key.contains("-") else { return codingKey }
        let words = key.components(separatedBy: "-")
        let camelCased = words[0] + words[1...].map(\.capitalized).joined()
        return AnyCodingKey(stringValue: camelCased)!
    }
    
    static var convertFromKebabCaseOrSnakeCase: JSONDecoder.KeyDecodingStrategy = .custom { keys in
        let codingKey = keys.last!
        let key = codingKey.stringValue
        
        if key.contains("-") {
            let words = key.components(separatedBy: "-")
            let camelCased = words[0] + words[1...].map(\.capitalized).joined()
            return AnyCodingKey(stringValue: camelCased)!
        }
        else if key.contains("_") {
            let words = key.components(separatedBy: "_")
            let camelCased = words[0] + words[1...].map(\.capitalized).joined()
            return AnyCodingKey(stringValue: camelCased)!
        }
        else {
            return codingKey
        }
    }
    
    struct AnyCodingKey: CodingKey {
        var stringValue: String
        init?(stringValue: String) {
            self.stringValue = stringValue
            self.intValue = nil
        }
        var intValue: Int?
        init?(intValue: Int) {
            self.intValue = intValue
            self.stringValue = "\(intValue)"
        }
    }
}

public struct JSON {
    public static let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromKebabCaseOrSnakeCase
        return decoder
    }()
    
    public static let encoder: JSONEncoder = {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [
            .prettyPrinted,
            .sortedKeys,
            .withoutEscapingSlashes
        ]
        encoder.keyEncodingStrategy = .convertToSnakeCase
        return encoder
    }()
}

public protocol JsonRepresentable where Self: Encodable {
    func jsonRepresentation() throws -> String?
}

public extension JsonRepresentable {
    func jsonRepresentation() throws -> String? {
        let data = try JSON.encoder.encode(self)
        return String(data: data, encoding: .utf8)
    }
}
