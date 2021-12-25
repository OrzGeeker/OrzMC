//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct AssetIndex: Codable {
    let id: String
    let sha1: String
    let size: Int64
    let totalSize: Int64
    let url: URL
    
    public var assetInfo: AssetInfo? {
        get async throws {
            guard let data = try await data(with: self.url)
            else {
                return nil
            }
            return try Mojang.jsonDecoder.decode(AssetInfo.self, from: data)
        }
    }
}

public struct AssetInfo: Codable, MojangJsonRepresentable {
    let objects: [String: Info]
    struct Info: Codable {
        let hash: String
        let size: Int64
    }
}
