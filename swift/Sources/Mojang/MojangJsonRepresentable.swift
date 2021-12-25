//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public protocol MojangJsonRepresentable where Self: Encodable {
    func jsonRepresentation() throws -> String?
}

public extension MojangJsonRepresentable {
    func jsonRepresentation() throws -> String? {
        let data = try  Mojang.jsonEncoder.encode(self)
        return String(data: data, encoding: .utf8)
    }
}
