//
//  File.swift
//  
//
//  Created by joker on 2022/1/15.
//

import XCTest
@testable import JokerKits
import Dispatch
import ObjectiveC

final class JokerKitsTests: XCTestCase {
    
    func testJSON() throws {
        
        // 测试解码
        let jsonString = """
        {
            "camelCase": "camel case value",
            "snake_case": "snake case value",
            "kebab-case": "kebab case value",
        }
        """
        
        struct TestModel: Codable, JsonRepresentable {
            let camelCase: String
            let snakeCase: String
            let kebabCase: String
        }
        
        let model = try JSON.decoder.decode(TestModel.self, from: jsonString.data(using: .utf8)!)
        XCTAssertEqual(model.camelCase, "camel case value")
        XCTAssertEqual(model.snakeCase, "snake case value")
        XCTAssertEqual(model.kebabCase, "kebab case value")
        
        // 测试编码
        let expectResult = """
        {
          "camel_case" : "camel case value",
          "kebab_case" : "kebab case value",
          "snake_case" : "snake case value"
        }
        """
        let data = try JSON.encoder.encode(model)
        let jsonContent = String(data: data, encoding: .utf8)!
        XCTAssertEqual(jsonContent, expectResult)
        XCTAssertEqual(try model.jsonRepresentation(), expectResult)
    }
    
    func testSyncShell() throws {
        let ret = try Shell.run(path: "/usr/bin/env", args: [
            "which",
            "bash"
        ])
        XCTAssertEqual(ret, "/bin/bash\n")
    }
    
    func testASyncShell() async throws {
        let process = try await Shell.run(path: "/usr/bin/env", args: [
          "which",
          "bash"
        ])
        XCTAssertEqual(process.terminationStatus, 0)
    }
    
    func testCallbackShell() throws {
        let stopGroup = DispatchGroup()
        stopGroup.enter()
        try Shell.run(path: "/usr/bin/env", args: [
            "which",
            "bash"
        ]) { process in
            XCTAssertEqual(process.terminationStatus, 0)
            stopGroup.leave()
        }
        stopGroup.wait()
    }
    
    func testDirOperations() throws {
        
        let tempDir = NSTemporaryDirectory()
        let testDirPath = NSString.path(withComponents: [
            tempDir,
            "test"
        ])
        
        if testDirPath.isDirPath() {
            try FileManager.default.removeItem(atPath: testDirPath)
        }
        
        let path = NSString.path(withComponents: [
            tempDir,
            "test",
            "dir"
        ])
        try path.makeDirIfNeed()
        XCTAssertTrue(path.isDirPath())
        
        let targetPath = NSString.path(withComponents: [
            tempDir,
            "test",
            "target"
        ])
        
        try FileManager.moveFile(fromFilePath: path, toFilePath: targetPath, overwrite: true)
        XCTAssert(targetPath.isDirPath())
        
        if let dirs = try FileManager.allSubDir(in: testDirPath) {
            XCTAssert(dirs.count == 1)
            XCTAssertEqual(NSString.path(withComponents: [testDirPath, dirs.first!]), targetPath)
        }
        
        let notExistDir = NSString.path(withComponents: [
            tempDir,
            "not",
            "exist"
        ])
        var textFiles = FileManager.allFiles(in: notExistDir, ext: "txt")
        XCTAssertNil(textFiles)
        
        textFiles = FileManager.allFiles(in: testDirPath, ext: "txt")
        XCTAssertNotNil(textFiles)
        if let textFiles = textFiles {
            XCTAssertEqual(textFiles.count, 0)
        }
        
        let testFilePath = NSString.path(withComponents: [
            tempDir,
            "test",
            "testFile.txt"
        ])
        FileManager.default.createFile(atPath: testFilePath, contents: "Just A Test File".data(using: .utf8))
        
        textFiles = FileManager.allFiles(in: testDirPath, ext: "txt")
        XCTAssertNotNil(textFiles)
        if let textFiles = textFiles {
            let index = textFiles.firstIndex(of: testFilePath)
            XCTAssertNotNil(index)
        }
    }
    
    func testJDKInstall() async throws {
        
        let javaVersion = try JavaInstaller.currentJavaVersion()
        print(javaVersion)
        
    }
    
    func testJDKUninstall() throws {
        if let javas = try JavaInstaller.installedJavaVersions() {
            print(javas)
        }
    }
}

