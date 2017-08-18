package bench1

func FindElementIdx(arrays []int, value int) int {
        for idx, v := range arrays {
                if v == value {
                        return idx
                }
        }

        return -1;
}
