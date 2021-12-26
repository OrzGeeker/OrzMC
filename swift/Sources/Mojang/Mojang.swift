//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/7.
//

import Foundation
import JokerKits

public struct Mojang {
    /// 获取版本信息
    public static var manifest: Manifest? {
        get async throws {
            let url = URL(string: "https://launchermeta.mojang.com/mc/game/version_manifest.json")
            guard let data = try await url?.getData
            else {
                return nil
            }
            return try JokerKits.JSON.decoder.decode(Manifest.self, from: data)
        }
    }
}
