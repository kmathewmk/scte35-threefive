import sys
from functools import partial
from threefive import Stream


class ResetCC(Stream):
    def re_cc(self, proxy=True, fixed_file="re_cced.ts"):
        """
        Stream.re_cc resets the continuity counters.
        MPEGTS packets are written to stdout for piping.
        """
        re_filed = fixed_file
        if not self._find_start():
            return False
        pcount = 128
        outfile = sys.stdout.buffer
        if not proxy:
            outfile = open(re_filed, "wb+")
        for chunk in iter(partial(self._tsdata.read, self._PACKET_SIZE * pcount), b""):
            chunky = memoryview(bytearray(chunk))
            chunks = [
                self._set_cc(chunky[i : i + self._PACKET_SIZE])
                for i in range(0, len(chunky), self._PACKET_SIZE)
            ]
            outfile.write(b"".join(chunks))
            chunky.release()
        self._tsdata.close()
        if not proxy:
            outfile.close()
            print(f"\nwrote {re_filed}\n")
        return True

    def re_cc_file(self, fixed_file):
        return self.re_cc(False, fixed_file)

    def _set_cc(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid == 0x1FFF:
            return pkt
        new_cc = 0
        if pid in self.maps.pid_cc:
            last_cc = self.maps.pid_cc[pid]
            new_cc = (last_cc + 1) % 16
        #        print(f"{new_cc}", end='\r')
        pkt[3] &= 0xF0
        pkt[3] += new_cc
        self.maps.pid_cc[pid] = new_cc
        return pkt


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 re_cc.py in_file.ts out_file.ts")
        sys.exit()
    inarg = sys.argv[1]
    outarg = sys.argv[2]
    resetter = ResetCC(inarg)
    resetter.re_cc_file(outarg)
