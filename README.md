# Lateral Movement Toolkit

> Post-Exploitation Lateral Movement Techniques for Red Teams

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-red)

## Overview

A modular toolkit implementing real-world lateral movement techniques used in advanced red team operations across Windows and Linux environments.

## Techniques

- WMI & WinRM remote execution
- SMB-based lateral movement (PsExec style)
- DCOM object abuse
- SSH key harvesting & reuse
- Token impersonation & privilege abuse
- Credential reuse automation

## Quick Start

```bash
git clone https://github.com/Youssefzdb/lateral-movement
cd lateral-movement
pip install -r requirements.txt
python lateral.py --target 192.168.1.10 --method wmi --user admin
```

## Legal Disclaimer

> For authorized red team operations and lab environments only.

## Author

**Youssef Zeidi** | Red Team Specialist | [GitHub](https://github.com/Youssefzdb)
