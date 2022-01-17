//
//  Platform.swift
//  
//
//  Created by joker on 2022/1/4.
//

/// [Swift条件编译参考](https://docs.swift.org/swift-book/ReferenceManual/Statements.html#//apple_ref/doc/uid/TP40014097-CH33-ID538)

public enum Platform {
    case linux
    case macosx
    case windows
    case unsupportedOS
    
    public static func os() -> Platform {
#if os(macOS)
        return .macosx
#elseif os(Windows)
        return .windows
#elseif os(Linux)
        return .linux
#else
        return .unsupportedOS
#endif
    }
    
    public enum Arch {
        case unknowned
        case i386
        case x86_64
        case arm
        case arm64
    }
    
    public static func arch() -> Arch {
#if arch(x86_64)
        return .x86_64
#elseif arch(arm)
        return .arm
#elseif arch(arm64)
        return .arm64
#elseif arch(i386)
        return .i386
#else
        return .unknowned
#endif
    }
}


