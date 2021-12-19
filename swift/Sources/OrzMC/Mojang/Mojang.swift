//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/7.
//

import Foundation

public struct Mojang {
    public enum Api: String {
        case manifest = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        case versions = "https://resources.download.minecraft.net"
        
        public func response() async throws -> String? {
            guard let url = URL(string: self.rawValue)
            else {
                return nil
            }
            let (data, response) = try await URLSession.shared.data(from: url)
            guard (response as? HTTPURLResponse)?.statusCode == 200
            else {
                return nil
            }
            let ret = String(data: data, encoding: .utf8)
            return ret
        }
    }
}
