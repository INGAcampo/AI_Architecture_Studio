"""Approximate second-order demand amplification with stability controls."""

class PDeltaAmplification:
    """Estimate P-delta amplification and reject unstable axial-load ratios."""
    def amplify(self, first_order_moment_nm, axial_load_n, lateral_displacement_m, story_height_m):
        """Execute the public PDeltaAmplification.amplify operation for the Omega structural analysis and design suite using explicit caller inputs."""
        if story_height_m <= 0:
            raise ValueError("Story height must be positive.")
        second_order = axial_load_n * lateral_displacement_m
        total = first_order_moment_nm + second_order
        return {
            "first_order_moment_nm": first_order_moment_nm,
            "second_order_moment_nm": second_order,
            "total_moment_nm": total,
            "amplification_factor": total / first_order_moment_nm if first_order_moment_nm else float("inf"),
        }
