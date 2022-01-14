// swift-tools-version:5.5
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "OrzMC",
    platforms: [
        .macOS(.v12)
    ],
    dependencies: [
        // Dependencies declare other packages that this package depends on.
        // .package(url: /* package url */, from: "1.0.0"),
        .package(url: "https://github.com/vapor/console-kit.git", from: "4.0.0"),
        .package(url: "https://github.com/apple/swift-crypto.git", "1.0.0" ..< "3.0.0"),
    ],
    targets: [
        // Targets are the basic building blocks of a package. A target can define a module or a test suite.
        // Targets can depend on other targets in this package, and on products in packages this package depends on.
        .target(
            name: "JokerKits",
            dependencies: [
                .product(name: "Crypto", package: "swift-crypto", condition: .when(platforms: [.linux])),
            ]
        ),
        
        .target(
            name: "Mojang",
            dependencies: ["JokerKits"]
        ),
        .testTarget(
            name: "MojangTests",
            dependencies: ["Mojang"]
        ),
        
        .executableTarget(
            name: "OrzMC",
            dependencies: [
                "Mojang",
                .product(name: "ConsoleKit", package: "console-kit"),
                "PaperMC"
            ]
        ),
        .testTarget(
            name: "OrzMCTests",
            dependencies: ["OrzMC"]
        ),
        
        .target(
            name: "PaperMC",
            dependencies: ["JokerKits"]
        ),
        .testTarget(
            name: "PaperMCTests",
            dependencies: ["PaperMC"]
        )
    ],
    swiftLanguageVersions: [.v5]
)
