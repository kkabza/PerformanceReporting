USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_ActivityPaymentDeposit]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_ActivityPaymentDeposit](
	[ActivityID] [int] NOT NULL,
	[Amount] [decimal](18, 3) NOT NULL
) ON [PRIMARY]
GO
