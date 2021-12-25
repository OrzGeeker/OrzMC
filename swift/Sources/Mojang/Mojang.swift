//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/7.
//

import Foundation

func data(with url: URL?) async throws -> Data? {
    guard let url = url
    else {
        return nil
    }
    let (data, response) = try await URLSession.shared.data(from: url)
    guard (response as? HTTPURLResponse)?.statusCode == 200
    else {
        return nil
    }
    return data
}

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
    public static var manifest: Manifest? {
        get async throws {
            let url = URL(string: "https://launchermeta.mojang.com/mc/game/version_manifest.json")
            guard let data = try await data(with: url)
            else {
                return nil
            }
            return try Mojang.jsonDecoder.decode(Manifest.self, from: data)
        }
    }
}
