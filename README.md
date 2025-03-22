# mcp-sonic-pi: MCP server for Sonic Pi

**mcp-sonic-pi** connects any MCP client with [Sonic Pi](https://sonic-pi.net/) enabling you to create music with English.

[📺 Demo](https://x.com/vortex_ape/status/1903470754999463969)

## Requirements

- Python 3.10+
- Sonic Pi installed and running

## Quickstart

Start using `mcp-sonic-pi` with an MCP client by running:

```bash
uvx mcp-sonic-pi
```

To start using this MCP server with Claude, add the following entry to your `claude_desktop_config.json`:

```
{
  "mcpServers": {
    "sonic-pi": {
      "args": [
        "mcp-sonic-pi"
      ],
      "command": "/path/to/uvx"
    }
  }
}
```

**Note**: Ensure Sonic Pi is running before starting the MCP server.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
