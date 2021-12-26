//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/26.
//

import Foundation

public struct JSON {
    public static let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder;
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
