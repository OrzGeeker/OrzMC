//
//  File.swift
//  
//
//  Created by joker on 2021/12/25.
//

import Foundation
import XCTest
@testable import OrzMC

final class MojangTests: XCTestCase {
    func testGameInfo() async throws {
        if let manifest = try await Mojang.manifest {
            let gameInfo = try await manifest.versions.first?.gameInfo
            let data = try Mojang.jsonEncoder.encode(gameInfo)
            let jsonString = String(data: data, encoding: .utf8)
            XCTAssertNotNil(jsonString)
        }
    }
}
