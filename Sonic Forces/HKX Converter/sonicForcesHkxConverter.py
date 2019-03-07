import struct
import sys
import base64
import os
import subprocess

animTemplate = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iYXNjaWkiPz4NCjxoa3RhZ2ZpbGUgdmVyc2lvbj0iMSI+DQogIDxjbGFzcyBuYW1lPSJoa1Jvb3RMZXZlbENvbnRhaW5lciIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJuYW1lZFZhcmlhbnRzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGtSb290TGV2ZWxDb250YWluZXJOYW1lZFZhcmlhbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrUm9vdExldmVsQ29udGFpbmVyTmFtZWRWYXJpYW50IiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9Im5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iY2xhc3NOYW1lIiB0eXBlPSJzdHJpbmciLz4NCiAgICA8bWVtYmVyIG5hbWU9InZhcmlhbnQiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGtCYXNlT2JqZWN0IiB2ZXJzaW9uPSIwIj4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrUmVmZXJlbmNlZE9iamVjdCIgdmVyc2lvbj0iMCIgcGFyZW50PSJoa0Jhc2VPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ibWVtU2l6ZUFuZEZsYWdzIiB0eXBlPSJ2b2lkIi8+DQogICAgPG1lbWJlciBuYW1lPSJyZWZlcmVuY2VDb3VudCIgdHlwZT0idm9pZCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthQW5pbWF0aW9uQ29udGFpbmVyIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJza2VsZXRvbnMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FTa2VsZXRvbiIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5pbWF0aW9ucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUFuaW1hdGlvbiIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmluZGluZ3MiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbmltYXRpb25CaW5kaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRhY2htZW50cyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUJvbmVBdHRhY2htZW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJza2lucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYU1lc2hCaW5kaW5nIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa2FTa2VsZXRvbiIgdmVyc2lvbj0iMyIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJwYXJlbnRJbmRpY2VzIiB0eXBlPSJpbnQiIGFycmF5PSJ0cnVlIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lcyIgdHlwZT0ic3RydWN0IiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUJvbmUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InJlZmVyZW5jZVBvc2UiIHR5cGU9InZlYzEyIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0icmVmZXJlbmNlRmxvYXRzIiB0eXBlPSJyZWFsIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZmxvYXRTbG90cyIgdHlwZT0ic3RyaW5nIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibG9jYWxGcmFtZXMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FTa2VsZXRvbkxvY2FsRnJhbWVPbkJvbmUiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUJvbmUiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJsb2NrVHJhbnNsYXRpb24iIHR5cGU9ImJ5dGUiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYVNrZWxldG9uTG9jYWxGcmFtZU9uQm9uZSIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJsb2NhbEZyYW1lIiB0eXBlPSJyZWYiIGNsYXNzPSJoa0xvY2FsRnJhbWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImJvbmVJbmRleCIgdHlwZT0iaW50Ii8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa0xvY2FsRnJhbWUiIHZlcnNpb249IjAiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFuaW1hdGlvbiIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0idHlwZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJkdXJhdGlvbiIgdHlwZT0icmVhbCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibnVtYmVyT2ZUcmFuc2Zvcm1UcmFja3MiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibnVtYmVyT2ZGbG9hdFRyYWNrcyIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJleHRyYWN0ZWRNb3Rpb24iIHR5cGU9InJlZiIgY2xhc3M9ImhrYUFuaW1hdGVkUmVmZXJlbmNlRnJhbWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImFubm90YXRpb25UcmFja3MiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbm5vdGF0aW9uVHJhY2siLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFuaW1hdGVkUmVmZXJlbmNlRnJhbWUiIHZlcnNpb249IjAiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFubm90YXRpb25UcmFjayIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJ0cmFja05hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5ub3RhdGlvbnMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbm5vdGF0aW9uVHJhY2tBbm5vdGF0aW9uIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa2FBbm5vdGF0aW9uVHJhY2tBbm5vdGF0aW9uIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9InRpbWUiIHR5cGU9InJlYWwiLz4NCiAgICA8bWVtYmVyIG5hbWU9InRleHQiIHR5cGU9InN0cmluZyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthQW5pbWF0aW9uQmluZGluZyIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ib3JpZ2luYWxTa2VsZXRvbk5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5pbWF0aW9uIiB0eXBlPSJyZWYiIGNsYXNzPSJoa2FBbmltYXRpb24iLz4NCiAgICA8bWVtYmVyIG5hbWU9InRyYW5zZm9ybVRyYWNrVG9Cb25lSW5kaWNlcyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZmxvYXRUcmFja1RvRmxvYXRTbG90SW5kaWNlcyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmxlbmRIaW50IiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUJvbmVBdHRhY2htZW50IiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJvcmlnaW5hbFNrZWxldG9uTmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lRnJvbUF0dGFjaG1lbnQiIHR5cGU9InZlYzE2Ii8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRhY2htZW50IiB0eXBlPSJyZWYiIGNsYXNzPSJoa1JlZmVyZW5jZWRPYmplY3QiLz4NCiAgICA8bWVtYmVyIG5hbWU9Im5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYm9uZUluZGV4IiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYU1lc2hCaW5kaW5nIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJtZXNoIiB0eXBlPSJyZWYiIGNsYXNzPSJoa3hNZXNoIi8+DQogICAgPG1lbWJlciBuYW1lPSJvcmlnaW5hbFNrZWxldG9uTmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJza2VsZXRvbiIgdHlwZT0icmVmIiBjbGFzcz0iaGthU2tlbGV0b24iLz4NCiAgICA8bWVtYmVyIG5hbWU9Im1hcHBpbmdzIiB0eXBlPSJyZWYiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGthTWVzaEJpbmRpbmdNYXBwaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lRnJvbVNraW5NZXNoVHJhbnNmb3JtcyIgdHlwZT0idmVjMTYiIGFycmF5PSJ0cnVlIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hNZXNoIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJzZWN0aW9ucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1lc2hTZWN0aW9uIi8+DQogICAgPG1lbWJlciBuYW1lPSJ1c2VyQ2hhbm5lbEluZm9zIiB0eXBlPSJyZWYiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4TWVzaFVzZXJDaGFubmVsSW5mbyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWVzaFNlY3Rpb24iIHZlcnNpb249IjEiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgICA8bWVtYmVyIG5hbWU9InZlcnRleEJ1ZmZlciIgdHlwZT0icmVmIiBjbGFzcz0iaGt4VmVydGV4QnVmZmVyIi8+DQogICAgPG1lbWJlciBuYW1lPSJpbmRleEJ1ZmZlcnMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hJbmRleEJ1ZmZlciIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibWF0ZXJpYWwiIHR5cGU9InJlZiIgY2xhc3M9ImhreE1hdGVyaWFsIi8+DQogICAgPG1lbWJlciBuYW1lPSJ1c2VyQ2hhbm5lbHMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa1JlZmVyZW5jZWRPYmplY3QiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleEJ1ZmZlciIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0iZGF0YSIgdHlwZT0ic3RydWN0IiBjbGFzcz0iaGt4VmVydGV4QnVmZmVyVmVydGV4RGF0YSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZGVzYyIgdHlwZT0ic3RydWN0IiBjbGFzcz0iaGt4VmVydGV4RGVzY3JpcHRpb24iLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleEJ1ZmZlclZlcnRleERhdGEiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0idmVjdG9yRGF0YSIgdHlwZT0idmVjNCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImZsb2F0RGF0YSIgdHlwZT0icmVhbCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQzMkRhdGEiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQxNkRhdGEiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQ4RGF0YSIgdHlwZT0iYnl0ZSIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9Im51bVZlcnRzIiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InZlY3RvclN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJmbG9hdFN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJ1aW50MzJTdHJpZGUiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idWludDE2U3RyaWRlIiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQ4U3RyaWRlIiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleERlc2NyaXB0aW9uIiB2ZXJzaW9uPSIxIj4NCiAgICA8bWVtYmVyIG5hbWU9ImRlY2xzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4VmVydGV4RGVzY3JpcHRpb25FbGVtZW50RGVjbCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4VmVydGV4RGVzY3JpcHRpb25FbGVtZW50RGVjbCIgdmVyc2lvbj0iMiI+DQogICAgPG1lbWJlciBuYW1lPSJieXRlT2Zmc2V0IiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InR5cGUiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idXNhZ2UiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYnl0ZVN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJudW1FbGVtZW50cyIgdHlwZT0iYnl0ZSIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4SW5kZXhCdWZmZXIiIHZlcnNpb249IjEiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgICA8bWVtYmVyIG5hbWU9ImluZGV4VHlwZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJpbmRpY2VzMTYiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImluZGljZXMzMiIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0idmVydGV4QmFzZU9mZnNldCIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJsZW5ndGgiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4QXR0cmlidXRlSG9sZGVyIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJhdHRyaWJ1dGVHcm91cHMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hBdHRyaWJ1dGVHcm91cCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4QXR0cmlidXRlR3JvdXAiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRyaWJ1dGVzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4QXR0cmlidXRlIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hBdHRyaWJ1dGUiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJ2YWx1ZSIgdHlwZT0icmVmIiBjbGFzcz0iaGtSZWZlcmVuY2VkT2JqZWN0Ii8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hNYXRlcmlhbCIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa3hBdHRyaWJ1dGVIb2xkZXIiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJzdGFnZXMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hNYXRlcmlhbFRleHR1cmVTdGFnZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZGlmZnVzZUNvbG9yIiB0eXBlPSJ2ZWM0Ii8+DQogICAgPG1lbWJlciBuYW1lPSJhbWJpZW50Q29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InNwZWN1bGFyQ29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImVtaXNzaXZlQ29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InN1Yk1hdGVyaWFscyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1hdGVyaWFsIi8+DQogICAgPG1lbWJlciBuYW1lPSJleHRyYURhdGEiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICAgIDxtZW1iZXIgbmFtZT0icHJvcGVydGllcyIgdHlwZT0ic3RydWN0IiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1hdGVyaWFsUHJvcGVydHkiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreE1hdGVyaWFsVGV4dHVyZVN0YWdlIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9InRleHR1cmUiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idXNhZ2VIaW50IiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InRjb29yZENoYW5uZWwiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWF0ZXJpYWxQcm9wZXJ0eSIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJrZXkiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idmFsdWUiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWVzaFVzZXJDaGFubmVsSW5mbyIgdmVyc2lvbj0iMCIgcGFyZW50PSJoa3hBdHRyaWJ1dGVIb2xkZXIiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJjbGFzc05hbWUiIHR5cGU9InN0cmluZyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthTWVzaEJpbmRpbmdNYXBwaW5nIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9Im1hcHBpbmciIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYVNwbGluZUNvbXByZXNzZWRBbmltYXRpb24iIHZlcnNpb249IjAiIHBhcmVudD0iaGthQW5pbWF0aW9uIj4NCiAgICA8bWVtYmVyIG5hbWU9Im51bUZyYW1lcyIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJudW1CbG9ja3MiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibWF4RnJhbWVzUGVyQmxvY2siIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibWFza0FuZFF1YW50aXphdGlvblNpemUiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmxvY2tEdXJhdGlvbiIgdHlwZT0icmVhbCIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmxvY2tJbnZlcnNlRHVyYXRpb24iIHR5cGU9InJlYWwiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImZyYW1lRHVyYXRpb24iIHR5cGU9InJlYWwiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImJsb2NrT2Zmc2V0cyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZmxvYXRCbG9ja09mZnNldHMiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InRyYW5zZm9ybU9mZnNldHMiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImZsb2F0T2Zmc2V0cyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZGF0YSIgdHlwZT0iYnl0ZSIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImVuZGlhbiIgdHlwZT0iaW50Ii8+DQogIDwvY2xhc3M+DQoNCiAgPG9iamVjdCBpZD0iIzAwMDEiIHR5cGU9ImhrUm9vdExldmVsQ29udGFpbmVyIj4NCiAgICA8YXJyYXkgbmFtZT0ibmFtZWRWYXJpYW50cyIgc2l6ZT0iMSI+DQogICAgICA8c3RydWN0Pg0KICAgICAgICA8c3RyaW5nIG5hbWU9Im5hbWUiPk1lcmdlZCBBbmltYXRpb24gQ29udGFpbmVyPC9zdHJpbmc+DQogICAgICAgIDxzdHJpbmcgbmFtZT0iY2xhc3NOYW1lIj5oa2FBbmltYXRpb25Db250YWluZXI8L3N0cmluZz4NCiAgICAgICAgPHJlZiBuYW1lPSJ2YXJpYW50Ij4jMDAwMjwvcmVmPg0KICAgICAgPC9zdHJ1Y3Q+DQogICAgPC9hcnJheT4NCiAgPC9vYmplY3Q+DQogIDxvYmplY3QgaWQ9IiMwMDAyIiB0eXBlPSJoa2FBbmltYXRpb25Db250YWluZXIiPg0KICAgIDxhcnJheSBuYW1lPSJhbmltYXRpb25zIiBzaXplPSIxIj4NCiAgICAgIDxyZWY+IzAwMDM8L3JlZj4NCiAgICA8L2FycmF5Pg0KICAgIDxhcnJheSBuYW1lPSJiaW5kaW5ncyIgc2l6ZT0iMSI+"
skelTemplate = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iYXNjaWkiPz4NCjxoa3RhZ2ZpbGUgdmVyc2lvbj0iMSI+DQogIDxjbGFzcyBuYW1lPSJoa1Jvb3RMZXZlbENvbnRhaW5lciIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJuYW1lZFZhcmlhbnRzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGtSb290TGV2ZWxDb250YWluZXJOYW1lZFZhcmlhbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrUm9vdExldmVsQ29udGFpbmVyTmFtZWRWYXJpYW50IiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9Im5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iY2xhc3NOYW1lIiB0eXBlPSJzdHJpbmciLz4NCiAgICA8bWVtYmVyIG5hbWU9InZhcmlhbnQiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGtCYXNlT2JqZWN0IiB2ZXJzaW9uPSIwIj4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrUmVmZXJlbmNlZE9iamVjdCIgdmVyc2lvbj0iMCIgcGFyZW50PSJoa0Jhc2VPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ibWVtU2l6ZUFuZEZsYWdzIiB0eXBlPSJ2b2lkIi8+DQogICAgPG1lbWJlciBuYW1lPSJyZWZlcmVuY2VDb3VudCIgdHlwZT0idm9pZCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthQW5pbWF0aW9uQ29udGFpbmVyIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJza2VsZXRvbnMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FTa2VsZXRvbiIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5pbWF0aW9ucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUFuaW1hdGlvbiIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmluZGluZ3MiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbmltYXRpb25CaW5kaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRhY2htZW50cyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUJvbmVBdHRhY2htZW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJza2lucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYU1lc2hCaW5kaW5nIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa2FTa2VsZXRvbiIgdmVyc2lvbj0iMyIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJwYXJlbnRJbmRpY2VzIiB0eXBlPSJpbnQiIGFycmF5PSJ0cnVlIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lcyIgdHlwZT0ic3RydWN0IiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhrYUJvbmUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InJlZmVyZW5jZVBvc2UiIHR5cGU9InZlYzEyIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0icmVmZXJlbmNlRmxvYXRzIiB0eXBlPSJyZWFsIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZmxvYXRTbG90cyIgdHlwZT0ic3RyaW5nIiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibG9jYWxGcmFtZXMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FTa2VsZXRvbkxvY2FsRnJhbWVPbkJvbmUiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUJvbmUiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJsb2NrVHJhbnNsYXRpb24iIHR5cGU9ImJ5dGUiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYVNrZWxldG9uTG9jYWxGcmFtZU9uQm9uZSIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJsb2NhbEZyYW1lIiB0eXBlPSJyZWYiIGNsYXNzPSJoa0xvY2FsRnJhbWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImJvbmVJbmRleCIgdHlwZT0iaW50Ii8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa0xvY2FsRnJhbWUiIHZlcnNpb249IjAiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFuaW1hdGlvbiIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0idHlwZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJkdXJhdGlvbiIgdHlwZT0icmVhbCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibnVtYmVyT2ZUcmFuc2Zvcm1UcmFja3MiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibnVtYmVyT2ZGbG9hdFRyYWNrcyIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJleHRyYWN0ZWRNb3Rpb24iIHR5cGU9InJlZiIgY2xhc3M9ImhrYUFuaW1hdGVkUmVmZXJlbmNlRnJhbWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImFubm90YXRpb25UcmFja3MiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbm5vdGF0aW9uVHJhY2siLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFuaW1hdGVkUmVmZXJlbmNlRnJhbWUiIHZlcnNpb249IjAiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUFubm90YXRpb25UcmFjayIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJ0cmFja05hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5ub3RhdGlvbnMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa2FBbm5vdGF0aW9uVHJhY2tBbm5vdGF0aW9uIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa2FBbm5vdGF0aW9uVHJhY2tBbm5vdGF0aW9uIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9InRpbWUiIHR5cGU9InJlYWwiLz4NCiAgICA8bWVtYmVyIG5hbWU9InRleHQiIHR5cGU9InN0cmluZyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthQW5pbWF0aW9uQmluZGluZyIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0ib3JpZ2luYWxTa2VsZXRvbk5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYW5pbWF0aW9uIiB0eXBlPSJyZWYiIGNsYXNzPSJoa2FBbmltYXRpb24iLz4NCiAgICA8bWVtYmVyIG5hbWU9InRyYW5zZm9ybVRyYWNrVG9Cb25lSW5kaWNlcyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZmxvYXRUcmFja1RvRmxvYXRTbG90SW5kaWNlcyIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYmxlbmRIaW50IiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYUJvbmVBdHRhY2htZW50IiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJvcmlnaW5hbFNrZWxldG9uTmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lRnJvbUF0dGFjaG1lbnQiIHR5cGU9InZlYzE2Ii8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRhY2htZW50IiB0eXBlPSJyZWYiIGNsYXNzPSJoa1JlZmVyZW5jZWRPYmplY3QiLz4NCiAgICA8bWVtYmVyIG5hbWU9Im5hbWUiIHR5cGU9InN0cmluZyIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYm9uZUluZGV4IiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhrYU1lc2hCaW5kaW5nIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJtZXNoIiB0eXBlPSJyZWYiIGNsYXNzPSJoa3hNZXNoIi8+DQogICAgPG1lbWJlciBuYW1lPSJvcmlnaW5hbFNrZWxldG9uTmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJza2VsZXRvbiIgdHlwZT0icmVmIiBjbGFzcz0iaGthU2tlbGV0b24iLz4NCiAgICA8bWVtYmVyIG5hbWU9Im1hcHBpbmdzIiB0eXBlPSJyZWYiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGthTWVzaEJpbmRpbmdNYXBwaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJib25lRnJvbVNraW5NZXNoVHJhbnNmb3JtcyIgdHlwZT0idmVjMTYiIGFycmF5PSJ0cnVlIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hNZXNoIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJzZWN0aW9ucyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1lc2hTZWN0aW9uIi8+DQogICAgPG1lbWJlciBuYW1lPSJ1c2VyQ2hhbm5lbEluZm9zIiB0eXBlPSJyZWYiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4TWVzaFVzZXJDaGFubmVsSW5mbyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWVzaFNlY3Rpb24iIHZlcnNpb249IjEiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgICA8bWVtYmVyIG5hbWU9InZlcnRleEJ1ZmZlciIgdHlwZT0icmVmIiBjbGFzcz0iaGt4VmVydGV4QnVmZmVyIi8+DQogICAgPG1lbWJlciBuYW1lPSJpbmRleEJ1ZmZlcnMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hJbmRleEJ1ZmZlciIvPg0KICAgIDxtZW1iZXIgbmFtZT0ibWF0ZXJpYWwiIHR5cGU9InJlZiIgY2xhc3M9ImhreE1hdGVyaWFsIi8+DQogICAgPG1lbWJlciBuYW1lPSJ1c2VyQ2hhbm5lbHMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa1JlZmVyZW5jZWRPYmplY3QiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleEJ1ZmZlciIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa1JlZmVyZW5jZWRPYmplY3QiPg0KICAgIDxtZW1iZXIgbmFtZT0iZGF0YSIgdHlwZT0ic3RydWN0IiBjbGFzcz0iaGt4VmVydGV4QnVmZmVyVmVydGV4RGF0YSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZGVzYyIgdHlwZT0ic3RydWN0IiBjbGFzcz0iaGt4VmVydGV4RGVzY3JpcHRpb24iLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleEJ1ZmZlclZlcnRleERhdGEiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0idmVjdG9yRGF0YSIgdHlwZT0idmVjNCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImZsb2F0RGF0YSIgdHlwZT0icmVhbCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQzMkRhdGEiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQxNkRhdGEiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQ4RGF0YSIgdHlwZT0iYnl0ZSIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9Im51bVZlcnRzIiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InZlY3RvclN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJmbG9hdFN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJ1aW50MzJTdHJpZGUiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idWludDE2U3RyaWRlIiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InVpbnQ4U3RyaWRlIiB0eXBlPSJpbnQiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreFZlcnRleERlc2NyaXB0aW9uIiB2ZXJzaW9uPSIxIj4NCiAgICA8bWVtYmVyIG5hbWU9ImRlY2xzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4VmVydGV4RGVzY3JpcHRpb25FbGVtZW50RGVjbCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4VmVydGV4RGVzY3JpcHRpb25FbGVtZW50RGVjbCIgdmVyc2lvbj0iMiI+DQogICAgPG1lbWJlciBuYW1lPSJieXRlT2Zmc2V0IiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InR5cGUiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idXNhZ2UiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0iYnl0ZVN0cmlkZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJudW1FbGVtZW50cyIgdHlwZT0iYnl0ZSIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4SW5kZXhCdWZmZXIiIHZlcnNpb249IjEiIHBhcmVudD0iaGtSZWZlcmVuY2VkT2JqZWN0Ij4NCiAgICA8bWVtYmVyIG5hbWU9ImluZGV4VHlwZSIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJpbmRpY2VzMTYiIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImluZGljZXMzMiIgdHlwZT0iaW50IiBhcnJheT0idHJ1ZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0idmVydGV4QmFzZU9mZnNldCIgdHlwZT0iaW50Ii8+DQogICAgPG1lbWJlciBuYW1lPSJsZW5ndGgiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4QXR0cmlidXRlSG9sZGVyIiB2ZXJzaW9uPSIxIiBwYXJlbnQ9ImhrUmVmZXJlbmNlZE9iamVjdCI+DQogICAgPG1lbWJlciBuYW1lPSJhdHRyaWJ1dGVHcm91cHMiIHR5cGU9InJlZiIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hBdHRyaWJ1dGVHcm91cCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4QXR0cmlidXRlR3JvdXAiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJhdHRyaWJ1dGVzIiB0eXBlPSJzdHJ1Y3QiIGFycmF5PSJ0cnVlIiBjbGFzcz0iaGt4QXR0cmlidXRlIi8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hBdHRyaWJ1dGUiIHZlcnNpb249IjAiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJ2YWx1ZSIgdHlwZT0icmVmIiBjbGFzcz0iaGtSZWZlcmVuY2VkT2JqZWN0Ii8+DQogIDwvY2xhc3M+DQogIDxjbGFzcyBuYW1lPSJoa3hNYXRlcmlhbCIgdmVyc2lvbj0iMSIgcGFyZW50PSJoa3hBdHRyaWJ1dGVIb2xkZXIiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJzdGFnZXMiIHR5cGU9InN0cnVjdCIgYXJyYXk9InRydWUiIGNsYXNzPSJoa3hNYXRlcmlhbFRleHR1cmVTdGFnZSIvPg0KICAgIDxtZW1iZXIgbmFtZT0iZGlmZnVzZUNvbG9yIiB0eXBlPSJ2ZWM0Ii8+DQogICAgPG1lbWJlciBuYW1lPSJhbWJpZW50Q29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InNwZWN1bGFyQ29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9ImVtaXNzaXZlQ29sb3IiIHR5cGU9InZlYzQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InN1Yk1hdGVyaWFscyIgdHlwZT0icmVmIiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1hdGVyaWFsIi8+DQogICAgPG1lbWJlciBuYW1lPSJleHRyYURhdGEiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICAgIDxtZW1iZXIgbmFtZT0icHJvcGVydGllcyIgdHlwZT0ic3RydWN0IiBhcnJheT0idHJ1ZSIgY2xhc3M9ImhreE1hdGVyaWFsUHJvcGVydHkiLz4NCiAgPC9jbGFzcz4NCiAgPGNsYXNzIG5hbWU9ImhreE1hdGVyaWFsVGV4dHVyZVN0YWdlIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9InRleHR1cmUiIHR5cGU9InJlZiIgY2xhc3M9ImhrUmVmZXJlbmNlZE9iamVjdCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idXNhZ2VIaW50IiB0eXBlPSJpbnQiLz4NCiAgICA8bWVtYmVyIG5hbWU9InRjb29yZENoYW5uZWwiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWF0ZXJpYWxQcm9wZXJ0eSIgdmVyc2lvbj0iMCI+DQogICAgPG1lbWJlciBuYW1lPSJrZXkiIHR5cGU9ImludCIvPg0KICAgIDxtZW1iZXIgbmFtZT0idmFsdWUiIHR5cGU9ImludCIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGt4TWVzaFVzZXJDaGFubmVsSW5mbyIgdmVyc2lvbj0iMCIgcGFyZW50PSJoa3hBdHRyaWJ1dGVIb2xkZXIiPg0KICAgIDxtZW1iZXIgbmFtZT0ibmFtZSIgdHlwZT0ic3RyaW5nIi8+DQogICAgPG1lbWJlciBuYW1lPSJjbGFzc05hbWUiIHR5cGU9InN0cmluZyIvPg0KICA8L2NsYXNzPg0KICA8Y2xhc3MgbmFtZT0iaGthTWVzaEJpbmRpbmdNYXBwaW5nIiB2ZXJzaW9uPSIwIj4NCiAgICA8bWVtYmVyIG5hbWU9Im1hcHBpbmciIHR5cGU9ImludCIgYXJyYXk9InRydWUiLz4NCiAgPC9jbGFzcz4NCg0KICA8b2JqZWN0IGlkPSIjMDAwMSIgdHlwZT0iaGtSb290TGV2ZWxDb250YWluZXIiPg0KICAgIDxhcnJheSBuYW1lPSJuYW1lZFZhcmlhbnRzIiBzaXplPSIxIj4NCiAgICAgIDxzdHJ1Y3Q+DQogICAgICAgIDxzdHJpbmcgbmFtZT0ibmFtZSI+TWVyZ2VkIEFuaW1hdGlvbiBDb250YWluZXI8L3N0cmluZz4NCiAgICAgICAgPHN0cmluZyBuYW1lPSJjbGFzc05hbWUiPmhrYUFuaW1hdGlvbkNvbnRhaW5lcjwvc3RyaW5nPg0KICAgICAgICA8cmVmIG5hbWU9InZhcmlhbnQiPiMwMDAyPC9yZWY+DQogICAgICA8L3N0cnVjdD4NCiAgICA8L2FycmF5Pg0KICA8L29iamVjdD4NCiAgPG9iamVjdCBpZD0iIzAwMDIiIHR5cGU9ImhrYUFuaW1hdGlvbkNvbnRhaW5lciI+DQogICAgPGFycmF5IG5hbWU9InNrZWxldG9ucyIgc2l6ZT0iMSI+DQogICAgICA8cmVmPiMwMDAzPC9yZWY+DQogICAgPC9hcnJheT4NCiAgPC9vYmplY3Q+DQogIDxvYmplY3QgaWQ9IiMwMDAzIiB0eXBlPSJoa2FTa2VsZXRvbiI+"

class hkTagItemArray(object):
    def __init__(self):
        self.itemType = None
        self.itemsOffset = 0
        self.itemCount = 0
        
    def seek(self, r):
        r.seek(self.itemsOffset)
        
    def readFormatByCount(self, r, format):
        self.seek(r)
        return [r.readFormat(format) for x in xrange(self.itemCount)]
        
    def readFormat(self, r, format):
        self.seek(r)
        return r.readFormat(format)
        
    def readByCount(self, r, size):
        self.seek(r)
        return r.read(self.itemCount * size)
        
    def readString(self, r):
        self.seek(r)
        return r.read(self.itemCount - 1)

class hkTagType(object):
    def __init__(self, name="", subTypeIndices=[]):
        self.name = name
        self.subTypeIndices = subTypeIndices

class hkTagReader(object):
    def __init__(self, f):
        self.f = f
        
        self.dataOffset = 0
        self.types = [hkTagType("null")]
        self.arrays = []
        
        self.parse()
        
    @staticmethod
    def fromFile(path):
        return hkTagReader(open(path, "rb"))
        
    def findType(self, name):
        for typ in self.types:
            if typ.name == name:
                return typ
        
    def findArray(self, typ):
        if hasattr(typ, "__len__"):
            typ = self.findType(typ)
            
        for array in self.arrays:
            if array.itemType == typ:
                return array

    def openSection(self, signature="", skip=False):
        offset = self.tell()
        size = self.readFormat(">I")
        size &= 0x3FFFFFFF
        
        sig = self.read(4)
        if signature != "" and signature != sig:
            raise ValueError("unexpected signature {}, wanted {}".format(sig, signature))
            
        if skip:
            self.seek(size - 8, 1)
            
        return (offset + 8, size - 8, offset + size)
        
    def parse(self):
        self.seek(0)
        
        self.openSection("TAG0")
        
        if self.read(self.openSection("SDKV")[1]) != "20160100":
            raise ValueError("unexpected tag version")
            
        self.dataOffset = self.openSection("DATA", True)[0]
        
        # Type Section
        self.openSection("TYPE")
        self.openSection("TPTR", True)
        
        typeStrings = self.read(self.openSection("TSTR")[1]).strip("\0").split("\0")
        
        end = self.openSection("TNAM")[2]
        prefix = self.readFormat("B")
        typeCount = self.readFormat("B")
        
        for i in xrange(typeCount - 1):
            index = self.readFormat("B")
            
            typ = hkTagType()
            typ.name = typeStrings[index]
            
            indicesCount = self.readFormat("B")
            for j in xrange(indicesCount):
                index1 = self.readFormat("B")             
                index2 = self.readFormat("B")
                
                if index2 == 0x80:
                    index2 = self.readFormat("B")
                
                typ.subTypeIndices.append((index1, index2))
            self.types.append(typ)
            
        self.seek(end)
            
        # later. this section is pure bit flag hell
        self.openSection("FSTR", True)
        self.openSection("TBOD", True)
        
        # Skip
        self.openSection("THSH", True)
        self.openSection("TPAD", True)
        
        self.openSection("INDX")
        end = self.openSection("ITEM")[2]
        
        while self.tell() < end:
            data = self.readFormat("<3I")
            
            array = hkTagItemArray()
            array.itemType = self.types[data[0] & 0xFF]
            array.itemsOffset = self.dataOffset + data[1]
            array.itemCount = data[2]
            
            self.arrays.append(array)
    
    def read(self, size):
        return self.f.read(size)
        
    def seek(self, offset, mode=0):
        self.f.seek(offset, mode)
        
    def tell(self):
        return self.f.tell()
    
    def readFormat(self, format):
        data = struct.unpack(format, self.read(struct.calcsize(format)))
        if len(data) == 1:
            return data[0]
        else:
            return data

    def readCString(self):
        result = ""
        char = self.read(1)

        while char != "\0":
            result += char
            char = self.read(1)

        return result

    def readArrayIndex(self, size=8):
        index = self.readFormat("<I")
        self.seek(size - 4, 1)
        
        if index == 0:
            return None
        else:
            return self.arrays[index]

def makeNode(name, attributes, indent):
    result = " " * indent + "<{}".format(name)
    
    if attributes != None:
        for key, value in attributes.iteritems():
            result += ' {}="{}"'.format(key, value)
    
    return result + ">\n"
        
def closeNode(name, indent):
    return " " * indent + "</{}>\n".format(name)
    
def makeLineNode(name, attributes, value, indent):
    return makeNode(name, attributes, indent)[:-1] + str(value) + closeNode(name, 0)

def toHavokFloat(value):
    return "x{:08x}".format(value)
    
def toHavokId(id):
    return "#" + str(id).zfill(4)

def combine(values, method=str):
    if len(values):
        if type(values[0]) == str:
            values[0] = values[0].lstrip()
        if type(values[-1]) == str:
            values[-1] = values[-1].rstrip("\n")
        return " ".join(map(method, values))

def toXmlExtension(i):
    return os.path.splitext(i)[0] + ".xml"
    
def toHkxExtension(i):
    return os.path.splitext(i)[0] + ".hkx"
    
def findAndConvertWithAssetCc2(i):
    argv = [x.lower() for x in sys.argv]

    path = "AssetCc2.exe"
    output = toHkxExtension(i)
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(sys.argv[0]), "AssetCc2.exe")
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(i), "AssetCc2.exe")
            if not os.path.exists(path):
                return
            
    if not ("-a" in argv and "-x" in argv):
        subprocess.call([path, "--strip", "--rules4101", i, output])
    if i != output and (not "-x" in argv):
        os.remove(i)

def makeHavokArrayNode(f, name, indent, values, method=str):
    if len(values):
        f.write(makeNode("array", {"name":name, "size":len(values)}, indent))
        f.write(" " * (indent + 2) + combine(values) + "\n")
        f.write(closeNode("array", indent))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Sonic Forces HKX Converter"
        print "Usage: [option] [file]"
        print "This script will convert .skl.hkx and .anm.hkx files from Sonic Forces to Sonic Generations compatible ones."
        print "If you have AssetCc2, the script will result a binary file as output and override changes to original file."
        print "Otherwise, it will output an XML file."
        print "\nIf you want to go simple, a drag and drop should work."
        print "\nOptions:"
        print "-x\tForce XML output."
        print "-a\tDon't do AssetCc2 conversion.\n\tNeeds also -x presented to work."
        print "\nMade by Skyth."
        print "\nPress any key to continue..."
        raw_input()
        sys.exit()

    for arg in sys.argv[1:]:
        if arg[0] != "-":
            inputFileName = arg
            break
    
    outputFileName = toXmlExtension(inputFileName)
   
    r = hkTagReader.fromFile(inputFileName)
    
    if inputFileName.lower().endswith(".anm.hkx"):
        binding = r.findArray("hkaAnimationBinding")
        
        binding.seek(r)
        r.seek(24, 1)
        
        originalSkeletonName = r.readArrayIndex()
        animation = r.readArrayIndex()
        transformTrackToBoneIndices = r.readArrayIndex(16)
        floatTrackToFloatSlotIndices = r.readArrayIndex(16)
        partitionIndices = r.readArrayIndex(16)
        blendHint = r.readFormat("<I")
        
        if animation.itemType.name != "hkaSplineCompressedAnimation":
            raise ValueError("Type {} is yet to be implemented!".format(animation.itemType.name))
    
        animation.seek(r)
        r.seek(24, 1)
        
        typ = r.readFormat("<I")
        duration = r.readFormat("<I")
        numberOfTransformTracks = r.readFormat("<I")
        numberOfFloatTracks = r.readFormat("<I")
        extractedMotion = r.readArrayIndex()
        annotationTracks = r.readArrayIndex(16)
        numFrames = r.readFormat("<I")
        numBlocks = r.readFormat("<I")
        maxFramesPerBlock = r.readFormat("<I")
        maskAndQuantizationSize = r.readFormat("<I")
        blockDuration = r.readFormat("<I")
        blockInverseDuration = r.readFormat("<I")
        frameDuration = r.readFormat("<I")
        
        r.seek(4, 1)
        
        blockOffsets = r.readArrayIndex(16)
        floatBlockOffsets = r.readArrayIndex(16)
        transformOffsets = r.readArrayIndex(16)
        floatOffsets = r.readArrayIndex(16)
        data = r.readArrayIndex(16)
        endian = r.readFormat("<I")
        
        annotations = [r.arrays[x[0]].readString(r) for x in annotationTracks.readFormatByCount(r, "<3Q")]
        
        with open(outputFileName, "w") as f:
            f.write(base64.b64decode(animTemplate) + "\n")
            
            annotationCount = len(annotations)
            
            f.write(makeLineNode("ref", None, toHavokId(4 + annotationCount), 6))
            f.write(closeNode("array", 4))
            f.write(closeNode("object", 2))
            
            f.write(makeNode("object", {"id":"#0003", "type":"hkaSplineCompressedAnimation"}, 2))
            f.write(makeLineNode("int", {"name":"type"}, typ, 4))
            f.write(makeLineNode("real", {"name":"duration"}, toHavokFloat(duration), 4))
            f.write(makeLineNode("int", {"name":"numberOfTransformTracks"}, numberOfTransformTracks, 4))
            makeHavokArrayNode(f, "annotationTracks", 4, [makeLineNode("ref", None, toHavokId(x), 5) for x in xrange(4, 4 + annotationCount)])
            f.write(makeLineNode("int", {"name":"numFrames"}, numFrames, 4))
            f.write(makeLineNode("int", {"name":"numBlocks"}, numBlocks, 4))
            f.write(makeLineNode("int", {"name":"maxFramesPerBlock"}, maxFramesPerBlock, 4))
            f.write(makeLineNode("int", {"name":"maskAndQuantizationSize"}, maskAndQuantizationSize, 4))
            f.write(makeLineNode("real", {"name":"blockDuration"}, toHavokFloat(blockDuration), 4))
            f.write(makeLineNode("real", {"name":"blockInverseDuration"}, toHavokFloat(blockInverseDuration), 4))
            f.write(makeLineNode("real", {"name":"frameDuration"}, toHavokFloat(frameDuration), 4))
            
            if blockOffsets != None:
                makeHavokArrayNode(f, "blockOffsets", 4, blockOffsets.readFormatByCount(r, "<I"))
            
            if floatBlockOffsets != None:
                makeHavokArrayNode(f, "floatBlockOffsets", 4, floatBlockOffsets.readFormatByCount(r, "<I"))
            
            if transformOffsets != None:
                makeHavokArrayNode(f, "transformOffsets", 4, transformOffsets.readFormatByCount(r, "<I"))
            
            if floatOffsets != None:
                makeHavokArrayNode(f, "floatOffsets", 4, floatOffsets.readFormatByCount(r, "<I"))
            
            if data != None:
                makeHavokArrayNode(f, "data", 4, data.readFormatByCount(r, "B"))
            
            f.write(makeLineNode("int", {"name":"endian"}, endian, 4))
            f.write(closeNode("object", 2))
            
            counter = 4
            for annotation in annotations:
                f.write(makeNode("object", {"id":toHavokId(counter), "type":"hkaAnnotationTrack"}, 2))
                f.write(makeLineNode("string", {"name":"trackName"}, annotation, 4))
                f.write(closeNode("object", 2))
                counter += 1
                
            f.write(makeNode("object", {"id":toHavokId(counter), "type":"hkaAnimationBinding"}, 2))
            f.write(makeLineNode("ref", {"name":"animation"}, "#0003", 4))
            
            if transformTrackToBoneIndices != None:
                makeHavokArrayNode(f, "transformTrackToBoneIndices", 4, transformTrackToBoneIndices.readFormatByCount(r, "<H"))
            
            if floatTrackToFloatSlotIndices != None:
                makeHavokArrayNode(f, "floatTrackToFloatSlotIndices", 4, floatTrackToFloatSlotIndices.readFormatByCount(r, "<H"))
            
            f.write(closeNode("object", 2))
            f.write(closeNode("hktagfile", 0))
            
        findAndConvertWithAssetCc2(outputFileName)
            
    elif inputFileName.lower().endswith(".skl.hkx"):
        skeleton = r.findArray("hkaSkeleton")
        parentIndices = r.findArray("hkInt16")
        bones = r.findArray("hkaBone")
        matrices = r.findArray("hkQsTransform")
        
        with open(outputFileName, "w") as f:
            f.write(base64.b64decode(skelTemplate) + "\n")
            
            # Indices
            makeHavokArrayNode(f, "parentIndices", 4, parentIndices.readFormatByCount(r, "<h"))
    
            # Bones
            f.write(makeNode("array", {"name":"bones", "size":bones.itemCount}, 4))
            
            for bone in bones.readFormatByCount(r, "<2Q"):
                f.write(makeNode("struct", None, 6))
                f.write(makeLineNode("string", {"name":"name"}, r.arrays[bone[0]].readString(r), 8))
                f.write(closeNode("struct", 6))
            
            f.write(closeNode("array", 4))
    
            # Matrices
            makeHavokArrayNode(f, "referencePose", 4, [makeLineNode("vec12", None, combine(x, toHavokFloat), 5) for x in matrices.readFormatByCount(r, "<12I")])
            f.write(closeNode("object", 2))
            f.write(closeNode("hktagfile", 0))

        findAndConvertWithAssetCc2(outputFileName)