//
//  File.swift
//  
//
//  Created by joker on 2021/12/25.
//

import XCTest
@testable import Mojang

final class MojangTests: XCTestCase {
    func testGameInfo() async throws {
        
        let manifest = try await Mojang.manifest
        XCTAssertNotNil(manifest, "Majong Manifest Info Fetch Failed!")
        
        let gameInfo = try await manifest?.versions.first?.gameInfo
        XCTAssertNotNil(gameInfo, "Game Version Info Fetch Failed!")
        
        let assetInfo = try await gameInfo?.assetIndex.assetInfo
        XCTAssertNotNil(assetInfo, "Game Asset Info Fetch Failed!")
                
    }
}
