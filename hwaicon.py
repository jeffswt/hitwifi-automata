
import io
import base64
import wx


def icon_from_base64(data):
    stream = io.BytesIO(base64.b64decode(data))
    image = wx.Image(stream)
    bitmap = wx.Bitmap(image)
    icon = wx.Icon()
    icon.CopyFromBitmap(bitmap)
    return icon


def get_icon():
    use_local_file = False
    if use_local_file:
        return wx.Icon('./assets/icon.png')
    s = ('iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEA'
         'mpwYAAAKdGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLv'
         'u78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxu'
         'czp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMx'
         'NDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJE'
         'RiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRh'
         'eC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0'
         'dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5v'
         'cmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5j'
         'b20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hh'
         'cC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMu'
         'YWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczpwaG90b3No'
         'b3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOnRpZmY9'
         'Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIiB4bWxuczpleGlmPSJodHRwOi8v'
         'bnMuYWRvYmUuY29tL2V4aWYvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90'
         'b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDE5LTA4LTA5'
         'VDEzOjMzOjI5KzA4OjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDE5LTA4LTA5VDE0OjIz'
         'OjEwKzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAxOS0wOC0wOVQxNDoyMzoxMCswODow'
         'MCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6'
         'NWI4ZTdhNjMtNGUxMC0zMzQyLThlN2EtZmU4Yzk1ZWI1MWNjIiB4bXBNTTpEb2N1bWVu'
         'dElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ZTA3MTFkMGEtYzdmYS04ODQzLTg3MWUt'
         'YzQwYWVmNjFjN2VlIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZjE4'
         'ODVhMmYtNTQ0OS02YjRmLThhOGItODc4M2VhOTI1MTYxIiBwaG90b3Nob3A6Q29sb3JN'
         'b2RlPSIzIiB0aWZmOk9yaWVudGF0aW9uPSIxIiB0aWZmOlhSZXNvbHV0aW9uPSI3MjAw'
         'MDAvMTAwMDAiIHRpZmY6WVJlc29sdXRpb249IjcyMDAwMC8xMDAwMCIgdGlmZjpSZXNv'
         'bHV0aW9uVW5pdD0iMiIgZXhpZjpDb2xvclNwYWNlPSI2NTUzNSIgZXhpZjpQaXhlbFhE'
         'aW1lbnNpb249IjIwMCIgZXhpZjpQaXhlbFlEaW1lbnNpb249IjIwMCI+IDx4bXBNTTpI'
         'aXN0b3J5PiA8cmRmOlNlcT4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNyZWF0ZWQiIHN0'
         'RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZjE4ODVhMmYtNTQ0OS02YjRmLThhOGItODc4'
         'M2VhOTI1MTYxIiBzdEV2dDp3aGVuPSIyMDE5LTA4LTA5VDEzOjMzOjI5KzA4OjAwIiBz'
         'dEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93'
         'cykiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlE'
         'PSJ4bXAuaWlkOjg1NWRmNDc5LTcyMTUtZjg0Mi05MzRiLWQ4Nzg5MTczNDIxNSIgc3RF'
         'dnQ6d2hlbj0iMjAxOS0wOC0wOVQxMzo1NTo1MyswODowMCIgc3RFdnQ6c29mdHdhcmVB'
         'Z2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKFdpbmRvd3MpIiBzdEV2dDpjaGFu'
         'Z2VkPSIvIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFu'
         'Y2VJRD0ieG1wLmlpZDozYzc2NTk3Yi0yNDNiLWQ4NGUtODY3My00MTdkNjcyMTk5OWEi'
         'IHN0RXZ0OndoZW49IjIwMTktMDgtMDlUMTQ6MjM6MTArMDg6MDAiIHN0RXZ0OnNvZnR3'
         'YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE5IChXaW5kb3dzKSIgc3RFdnQ6'
         'Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY29udmVydGVkIiBzdEV2'
         'dDpwYXJhbWV0ZXJzPSJmcm9tIGFwcGxpY2F0aW9uL3ZuZC5hZG9iZS5waG90b3Nob3Ag'
         'dG8gaW1hZ2UvcG5nIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJkZXJpdmVkIiBzdEV2'
         'dDpwYXJhbWV0ZXJzPSJjb252ZXJ0ZWQgZnJvbSBhcHBsaWNhdGlvbi92bmQuYWRvYmUu'
         'cGhvdG9zaG9wIHRvIGltYWdlL3BuZyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2'
         'ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NWI4ZTdhNjMtNGUxMC0zMzQyLThl'
         'N2EtZmU4Yzk1ZWI1MWNjIiBzdEV2dDp3aGVuPSIyMDE5LTA4LTA5VDE0OjIzOjEwKzA4'
         'OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAo'
         'V2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhp'
         'c3Rvcnk+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlk'
         'OjNjNzY1OTdiLTI0M2ItZDg0ZS04NjczLTQxN2Q2NzIxOTk5YSIgc3RSZWY6ZG9jdW1l'
         'bnRJRD0ieG1wLmRpZDpmMTg4NWEyZi01NDQ5LTZiNGYtOGE4Yi04NzgzZWE5MjUxNjEi'
         'IHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpmMTg4NWEyZi01NDQ5LTZi'
         'NGYtOGE4Yi04NzgzZWE5MjUxNjEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJE'
         'Rj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz72dUdsAAAKJUlEQVRYw61Y'
         'B1CU6RkGlQjnoRLPqHi2kEMT8QKMI8h5ouMpRk7PGxgde+ycjJyMGh1bDJZRsYKIBcSO'
         'WEaJvaIRKxqwcEp0QBQQKZbthd0/z7P5YJZ/dykXv5lnWHa//3uft7/f7yRJklNjsGPH'
         'jmbA9zt37ly/e/fuDKAUn434q01JSVELaLDHnJycXInvM3ft2pWQmJg4Gt+1kp9X72oI'
         'qW3btvklJSXtgbCXIGM+efKkMjs7W8rPz5fev38vqVQqqby8XHrz5o0F/KxQKCx4+fKl'
         '9PDhQ+nMmTMqnGEA6WKcc2Lr1q0D/y+C0NYNWs/HYTkHDx5UPnnyxCKYpCjw8uXLVXv2'
         '7DFinwQFjJs3b1bHxsYqiE2bNqkTEhL0tCKeN547d66Kz7x48UKqrKyU8vLypKNHjyrw'
         'Wz72xWBf20YRhHZRsJQhMzPTWFRUJBGnTp0iGXNMTEx5REREwYgRI3J69ux53MXFZRWO'
         'mQtEAFMFZgLRwPLu3bsfHjZsWNbMmTMLli1bVgqlq44dO2YoKCiQysrKpKysLAkhYMT3'
         'sXaJWhOD5j/ADaqMjAydRqORHjx4IJHU2rVrP4aEhNzE9r8D44GhQBDQC/g94Al8AXgI'
         '8HMHoCvQEwgEhgBjgEXBwcFXVqxYUUHrX79+3URZJAqjVMXFxUXYEFy9enUHxMalEydO'
         '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'
         'SUVORK5CYII=')
    return icon_from_base64(s)


def update_icon():
    f = open('./assets/icon.png', 'rb')
    d = base64.b64encode(f.read()).decode('utf-8')
    f.close()
    def chunk(l, n):
        a = []
        for i in range(0, len(l), n):
            a.append(l[i:i + n])
        return a
    p = ''.join('         \'' + i + '\'\n' for i in chunk(d, 68))
    p = '    s = (' + p[9:-1] + ')\n'
    print(p)


if __name__ == '__main__':
    update_icon()
